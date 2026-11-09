"""Stage 9 checks for service listing, integrated workflows and the menu."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pytest

from smartcare.console import parse_status, run_menu
from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


NINE = datetime(2026, 10, 1, 9)
PROJECT_DIR = Path(__file__).resolve().parents[1]


def session() -> tuple[SmartCareDataStore, AppointmentService]:
    """Register P1, D1 and D2 in a fresh store."""
    data_store = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioners = PractitionerService(data_store)
    practitioners.register_practitioner(
        'D1', 'Taylor Example', 'General practice',
    )
    practitioners.register_practitioner('D2', 'Jordan Example', 'Cardiology')
    return data_store, AppointmentService(data_store)


def ids(appointments: list[Appointment]) -> list[str]:
    """Return appointment IDs in order."""
    return [appointment.appointment_id for appointment in appointments]


# ----- QRY-04 service listing cases -----

def test_qry04_known_practitioner_without_appointments() -> None:
    """QRY-04: known practitioner, no appointments -> new empty list."""
    _, service = session()
    assert service.list_practitioner_appointments('D1') == []


def test_qry04_known_practitioner_without_matching_status() -> None:
    """QRY-04: known practitioner, no matching status -> empty list."""
    _, service = session()
    service.book_appointment('A1', 'P1', 'D1', NINE)
    assert service.list_practitioner_appointments(
        'D1', AppointmentStatus.CANCELLED,
    ) == []


def test_qry04_unknown_practitioner_raises_lookup_error() -> None:
    """QRY-04: valid but unknown ID -> LookupError."""
    _, service = session()
    with pytest.raises(LookupError):
        service.list_practitioner_appointments('D9')


def test_qry04_blank_or_invalid_id_raises_value_error() -> None:
    """QRY-04: blank or non-string ID -> ValueError."""
    _, service = session()
    for invalid_id in ['', '   ', None, 1]:
        with pytest.raises(ValueError):
            service.list_practitioner_appointments(invalid_id)


def test_qry04_text_status_raises_value_error() -> None:
    """QRY-04: 'scheduled' text is not an enum -> ValueError."""
    data_store, service = session()
    service.book_appointment('A1', 'P1', 'D1', NINE)
    with pytest.raises(ValueError):
        service.list_practitioner_appointments('D1', 'scheduled')
    assert ids(data_store.list_appointments()) == ['A1']


def test_qry04_omitted_status_keeps_history() -> None:
    """QRY-04: omitted status lists cancelled history too."""
    _, service = session()
    cancelled = service.book_appointment('A1', 'P1', 'D1', NINE)
    service.cancel_appointment('A1')
    result = service.list_practitioner_appointments('D1')
    assert result == [cancelled]
    assert result[0] is cancelled


def test_qry04_uses_registered_id_for_trimmed_input() -> None:
    """QRY-04: ' D1 ' finds D1's appointments, not a misleading empty list."""
    _, service = session()
    appointment = service.book_appointment('A1', 'P1', 'D1', NINE)
    assert service.list_practitioner_appointments(' D1 ') == [appointment]


def test_qry04_returns_fresh_list() -> None:
    """QRY-04: each call returns a new list."""
    _, service = session()
    service.book_appointment('A1', 'P1', 'D1', NINE)
    first = service.list_practitioner_appointments('D1')
    second = service.list_practitioner_appointments('D1')
    assert first == second
    assert first is not second


# ----- Integrated service workflow -----

def test_service_workflow_preserves_state_and_history() -> None:
    """Rejections keep state; history is kept; the freed slot is reused."""
    data_store, service = session()
    patients = PatientService(data_store)
    a1 = service.book_appointment('A1', 'P1', 'D1', NINE)

    before = data_store.list_appointments()
    with pytest.raises(ValueError):
        patients.register_patient('P1', 'Replacement')
    with pytest.raises(LookupError):
        service.book_appointment('A9', 'P9', 'D1', NINE)
    with pytest.raises(ValueError):
        service.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 2, 9))
    with pytest.raises(ValueError):
        service.book_appointment('A-CONFLICT', 'P1', 'D1', NINE)
    assert data_store.list_appointments() == before
    assert data_store.find_appointment('A-CONFLICT') is None
    assert data_store.find_patient('P1').name == 'Alex Example'

    a2 = service.book_appointment('A2', 'P1', 'D2', NINE)
    assert a2.status is AppointmentStatus.SCHEDULED

    service.cancel_appointment('A1')
    with pytest.raises(ValueError):
        service.cancel_appointment('A1')
    assert service.find_appointment('A1') is a1
    assert a1.status is AppointmentStatus.CANCELLED

    assert service.list_practitioner_appointments('D1') == [a1]
    assert service.list_practitioner_appointments(
        'D1', AppointmentStatus.SCHEDULED,
    ) == []

    a3 = service.book_appointment('A3', 'P1', 'D1', NINE)
    assert ids(service.list_practitioner_appointments('D1')) == ['A1', 'A3']
    assert ids(service.list_practitioner_appointments('D2')) == ['A2']
    assert data_store.list_appointments() == [a1, a2, a3]


# ----- Console status conversion -----

def test_parse_status_converts_console_text() -> None:
    """Blank means all; text maps to the enum; other text is rejected."""
    assert parse_status('') is None
    assert parse_status('  ') is None
    assert parse_status(' Scheduled ') is AppointmentStatus.SCHEDULED
    assert parse_status('cancelled') is AppointmentStatus.CANCELLED
    assert parse_status('completed') is AppointmentStatus.COMPLETED
    with pytest.raises(ValueError):
        parse_status('pending')


# ----- Console menu (UI-01 / UI-02) -----

def run_with(inputs: list[str]) -> list[str]:
    """Run the real menu with scripted input; return printed lines."""
    answers = iter(inputs)
    printed: list[str] = []

    def fake_input(prompt: str = '') -> str:
        """Behave like input(): raise EOFError when input runs out."""
        try:
            return next(answers)
        except StopIteration:
            raise EOFError from None

    run_menu(fake_input, printed.append)
    return printed


UI01_INPUTS = [
    '1', 'P1', 'Alex Example',
    '2', 'P1',
    '3', 'D1', 'Taylor Example', 'General practice',
    '4', 'D1',
    '3', 'D2', 'Jordan Example', 'Cardiology',
    '4', 'D2',
    '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
    '5', 'A-CONFLICT', 'P1', 'D1', '2026-10-01 09:00',
    '5', 'A2', 'P1', 'D2', '2026-10-01 09:00',
    '6', 'A1',
    '7', 'A1',
    '8', 'D1', '',
    '8', 'D1', 'scheduled',
    '5', 'A3', 'P1', 'D1', '2026-10-01 09:00',
    '8', 'D1', '',
    '0',
]


def test_ui01_full_menu_workflow() -> None:
    """UI-01: the complete demonstration run."""
    out = run_with(UI01_INPUTS)
    assert 'Patient found. P1: Alex Example' in out
    assert 'Practitioner found. D1: Taylor Example, General practice' in out
    assert 'Practitioner found. D2: Jordan Example, Cardiology' in out
    assert (
        'Error: Practitioner already has a SCHEDULED appointment '
        'at this time'
    ) in out
    assert '   Reference      : A2: P1 with D2, 2026-10-01 09:00, scheduled' in out
    assert 'Appointment cancelled successfully.' in out
    assert 'Appointment found.' in out
    assert 'Filter: Scheduled' in out
    assert 'No appointments found.' in out
    final_list = out[len(out) - out[::-1].index('Filter: All statuses'):]
    assert '1. A1' in final_list and '2. A3' in final_list
    assert '2 appointments found.' in final_list
    assert out[-1] == 'Goodbye. Session data discarded.'


UI02_INPUTS = [
    '1', 'P1', 'Alex Example',
    '3', 'D1', 'Taylor Example', 'General practice',
    '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
    '99',
    '2', '',
    '2', 'P9',
    '1', 'P1', 'Replacement',
    '5', 'A9', 'P9', 'D1', '2026-10-02 09:00',
    '5', 'BAD-TEXT', 'P1', 'D1', 'not a date',
    '5', 'BAD-DATE', 'P1', 'D1', '2026-02-30 09:00',
    '7', 'UNKNOWN',
    '6', 'A1',
    '6', 'A1',
    '8', 'D1', 'pending',
    '5', 'A9', 'P1', 'D1', '2026-10-02 09:00',
    '2', 'P1',
    '0',
]


def test_ui02_invalid_input_recovery() -> None:
    """UI-02: each error is reported and the session continues."""
    out = run_with(UI02_INPUTS)
    assert 'Unknown choice. Choose a number from 0 to 8.' in out
    assert 'Error: Patient ID cannot be blank' in out
    assert 'Error: Patient not found' in out
    assert 'Error: Patient ID already exists' in out
    assert 'Error: Use date/time format YYYY-MM-DD HH:MM' in out
    assert 'Error: Invalid calendar date/time; use YYYY-MM-DD HH:MM' in out
    assert 'Error: Appointment not found' in out
    assert 'Error: Only SCHEDULED appointments may be cancelled' in out
    assert 'Error: Status must be scheduled, cancelled or completed' in out
    # The rejected A9 booking did not reserve its ID: it books later.
    assert '   Reference      : A9: P1 with D1, 2026-10-02 09:00, scheduled' in out
    # The duplicate registration did not replace P1.
    assert out.count('Patient found. P1: Alex Example') == 1
    assert out[-1] == 'Goodbye. Session data discarded.'


def test_menu_exits_cleanly_when_input_ends() -> None:
    """End of input exits normally instead of crashing."""
    assert run_with([])[-1] == 'Goodbye. Session data discarded.'


def test_real_console_process_runs_ui01() -> None:
    """Run python main.py --interactive with redirected input."""
    completed = subprocess.run(
        [sys.executable, 'main.py', '--interactive'],
        input='\n'.join(UI01_INPUTS) + '\n',
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        timeout=30,
    )
    assert completed.returncode == 0
    assert 'Traceback' not in completed.stderr
    assert '2 appointments found.' in completed.stdout
    assert 'Goodbye. Session data discarded.' in completed.stdout


def test_new_session_starts_empty() -> None:
    """A new menu session has no records from an earlier one."""
    run_with(['1', 'P1', 'Alex Example', '0'])
    out = run_with(['2', 'P1', '0'])
    assert 'Error: Patient not found' in out