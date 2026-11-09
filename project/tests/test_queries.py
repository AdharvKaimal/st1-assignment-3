"""Stage 9 checks for the pure query functions in queries.py.

Fixtures are built directly from domain objects: the queries take
explicit inputs and do not need a data store or services.
"""

from datetime import datetime

from smartcare import queries
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import appointment_sort_key, select_appointments


NINE = datetime(2026, 10, 1, 9)
TEN = datetime(2026, 10, 1, 10)


def fixtures() -> list[Appointment]:
    """Return an unsorted source list for D1 and D2.

    A1 (cancelled), A3 (scheduled) and A5 (completed) share 09:00 with
    D1, so equal-time tie-breaks are tested without breaking the
    SCHEDULED conflict rule.
    """
    patient = Patient('P1', 'Alex Example')
    d1 = Practitioner('D1', 'Taylor Example', 'General practice')
    d2 = Practitioner('D2', 'Jordan Example', 'Cardiology')
    return [
        Appointment('A4', patient, d1, TEN),
        Appointment('A5', patient, d1, NINE, AppointmentStatus.COMPLETED),
        Appointment('A2', patient, d2, NINE),
        Appointment('A3', patient, d1, NINE),
        Appointment('A1', patient, d1, NINE, AppointmentStatus.CANCELLED),
    ]


def ids(appointments: list[Appointment]) -> list[str]:
    """Return appointment IDs in order."""
    return [appointment.appointment_id for appointment in appointments]


def snapshot(appointments: list[Appointment]) -> list[tuple]:
    """Record source order and every relevant field."""
    return [
        (
            appointment,
            appointment.appointment_id,
            appointment.patient,
            appointment.practitioner,
            appointment.date_time,
            appointment.status,
        )
        for appointment in appointments
    ]


# ----- QRY-01 practitioner selection -----

def test_qry01_only_requested_practitioner() -> None:
    """QRY-01: only D1 is returned; D2 is the control."""
    source = fixtures()
    assert ids(select_appointments(source, 'D1')) == ['A1', 'A3', 'A5', 'A4']
    assert ids(select_appointments(source, 'D2')) == ['A2']


def test_qry01_unmatched_practitioner_returns_empty() -> None:
    """QRY-01: a practitioner with no appointments gives an empty list."""
    assert select_appointments(fixtures(), 'D9') == []


# ----- QRY-02 status filtering -----

def test_qry02_default_includes_every_status() -> None:
    """QRY-02: status=None includes CANCELLED and COMPLETED."""
    statuses = {
        appointment.status
        for appointment in select_appointments(fixtures(), 'D1')
    }
    assert statuses == set(AppointmentStatus)


def test_qry02_each_explicit_status() -> None:
    """QRY-02: each enum status returns only that status."""
    source = fixtures()
    assert ids(select_appointments(
        source, 'D1', AppointmentStatus.SCHEDULED,
    )) == ['A3', 'A4']
    assert ids(select_appointments(
        source, 'D1', AppointmentStatus.CANCELLED,
    )) == ['A1']
    assert ids(select_appointments(
        source, 'D1', AppointmentStatus.COMPLETED,
    )) == ['A5']


def test_qry02_no_matching_status_is_empty() -> None:
    """QRY-02: a status with no matches gives an empty list."""
    assert select_appointments(
        fixtures(), 'D2', AppointmentStatus.CANCELLED,
    ) == []


# ----- QRY-03 ordering -----

def test_qry03_orders_by_time_then_id_and_keeps_source() -> None:
    """QRY-03: date/time order, equal-time ID tie-break, source kept."""
    source = fixtures()
    before = snapshot(source)
    result = select_appointments(source, 'D1')
    assert ids(result) == ['A1', 'A3', 'A5', 'A4']
    assert snapshot(source) == before


# ----- FP-01 repeatability and no hidden state -----

def test_fp01_repeated_calls_give_same_result() -> None:
    """FP-01: unchanged inputs give the same result each time."""
    source = fixtures()
    before = snapshot(source)
    first = select_appointments(source, 'D1', AppointmentStatus.SCHEDULED)
    second = select_appointments(source, 'D1', AppointmentStatus.SCHEDULED)
    assert first == second
    assert first is not second
    assert snapshot(source) == before


def test_fp01_no_output(capsys) -> None:
    """FP-01: queries print nothing."""
    select_appointments(fixtures(), 'D1')
    appointment_sort_key(fixtures()[0])
    assert capsys.readouterr().out == ''


# ----- FP-02 new list, same unchanged objects -----

def test_fp02_empty_source_gives_new_list() -> None:
    """FP-02: an empty source returns a distinct empty list."""
    source: list[Appointment] = []
    result = select_appointments(source, 'D1')
    assert result == []
    assert result is not source


def test_fp02_already_sorted_source_gives_new_list() -> None:
    """FP-02: an already-sorted source still returns a new list."""
    already_sorted = select_appointments(fixtures(), 'D1')
    result = select_appointments(already_sorted, 'D1')
    assert result == already_sorted
    assert result is not already_sorted


def test_fp02_unsorted_source_reuses_unchanged_objects() -> None:
    """FP-02: the new list holds the same objects, unchanged."""
    source = fixtures()
    before = snapshot(source)
    result = select_appointments(source, 'D1')
    assert result is not source
    for appointment in result:
        assert any(appointment is original for original in source)
    assert snapshot(source) == before


# ----- FP-03 named key -----

def test_fp03_named_key_value() -> None:
    """FP-03: the key returns (date_time, appointment_id)."""
    appointment = fixtures()[0]
    assert appointment_sort_key(appointment) == (TEN, 'A4')


def test_fp03_key_does_not_change_appointment() -> None:
    """FP-03: calling the key leaves the appointment unchanged."""
    source = fixtures()
    before = snapshot(source)
    for appointment in source:
        appointment_sort_key(appointment)
    assert snapshot(source) == before


def test_fp03_sorting_uses_named_key(monkeypatch) -> None:
    """FP-03: select_appointments calls appointment_sort_key."""
    calls: list[str] = []
    original_key = queries.appointment_sort_key

    def recording_key(appointment: Appointment) -> tuple[datetime, str]:
        calls.append(appointment.appointment_id)
        return original_key(appointment)

    monkeypatch.setattr(queries, 'appointment_sort_key', recording_key)
    queries.select_appointments(fixtures(), 'D1')
    assert sorted(calls) == ['A1', 'A3', 'A4', 'A5']