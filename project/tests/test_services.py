"""Stage 6 checks for lookup and cancellation service methods."""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def foundation() -> tuple[
    SmartCareDataStore,
    Patient,
    Practitioner,
    AppointmentService,
]:
    """Create fresh registered participants and services for a supplied
    check.
    """
    data_store = SmartCareDataStore()
    patient = PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioner = PractitionerService(
        data_store,
    ).register_practitioner('D1', 'Taylor Example', 'General')
    return (data_store, patient, practitioner, AppointmentService(data_store))

# ------------------------------------
#       Using tests from Part E
# ------------------------------------

# ----- PatientService.find_patient -----

def test_find_patient_returns_stored_object() -> None:
    """Known patient lookup: returns the same Patient that was stored"""
    data_store, patient, _, _ = foundation()
    assert PatientService(data_store).find_patient('P1') is patient

def test_find_patient_trims_ids() -> None:
    """Trimmed IDs: spaces around the ID are ignored"""
    data_store, patient, _, _ = foundation()
    assert PatientService(data_store).find_patient(' P1 ') is patient

def test_find_patient_is_case_sensitive() -> None:
    """Case-sensitive IDs: a different case ID is treated as unknown"""
    data_store, _, _, _ = foundation()
    with pytest.raises(LookupError):
        PatientService(data_store).find_patient('p1')

def test_find_patient_unknown_id() -> None:
    """Unknown lookup: a valid but unstored ID raises LookupError"""
    data_store, _, _, _ = foundation()
    with pytest.raises(LookupError):
        PatientService(data_store).find_patient('P2')

def test_find_patient_invalid_id() -> None:
    """Invalid IDs: blank or non-string IDs raise ValueError"""
    data_store, _, _, _ = foundation()
    for invalid_id in ['', ' ', None, 1]:
        with pytest.raises(ValueError):
            PatientService(data_store).find_patient(invalid_id)

# ----- PractitionerService.find_practitioner -----

def test_find_practitioner_returns_stored_object() -> None:
    """Known practitioner lookup: returns the same Practitioner that was stored"""
    data_store, _, practitioner, _ = foundation()
    assert PractitionerService(data_store).find_practitioner('D1') is practitioner

def test_find_practitioner_trims_ids() -> None:
    """Trimmed IDs: spaces around the ID are ignored"""
    data_store, _, practitioner, _ = foundation()
    assert PractitionerService(data_store).find_practitioner(' D1 ') is practitioner

def test_find_practitioner_is_case_sensitive() -> None:
    """Case-sensitive IDs: a different case ID is treated as unknown"""
    data_store, _, _, _ = foundation()
    with pytest.raises(LookupError):
        PractitionerService(data_store).find_practitioner('d1')

def test_find_practitioner_unknown_id() -> None:
    """Unknown lookup: a valid but unstored ID raises LookupError"""
    data_store, _, _, _ = foundation()
    with pytest.raises(LookupError):
        PractitionerService(data_store).find_practitioner('D2')

def test_find_practitioner_invalid_id() -> None:
    """Invalid IDs: blank or non-string IDs raise ValueError"""
    data_store, _, _, _ = foundation()
    for invalid_id in ['', ' ', None, 1]:
        with pytest.raises(ValueError):
            PractitionerService(data_store).find_practitioner(invalid_id)

# ----- AppointmentService.cancel_appointment -----

# Testing cancellation status and same-object return
def test_cancel_same_object_return_cancelled() -> None:
    """Cancellation and same-object return: cancelling a SCHEDULED appointment returns the same object but now CANCELLED"""
    _, _, _, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
    )
    result = appointment_service.cancel_appointment('A1')
    assert result is appointment
    assert result.status is AppointmentStatus.CANCELLED

def test_cancelled_appointment_is_stored() -> None:
    """Continued retrieval: the cancelled appointment is still in the store"""
    data_store, _, _, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
    )
    appointment_service.cancel_appointment('A1')
    assert appointment_service.find_appointment('A1') is appointment
    assert data_store.list_appointments() == [appointment]

def test_cancelled_twice_keeps_state() -> None:
    """Repeated cancellation: raises ValueError and keeps state unchanged"""
    data_store, _, _, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
        )
    result = appointment_service.cancel_appointment('A1')
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]

def test_cancel_from_completed_keeps_state() -> None:
    """Cancellation from COMPLETED: raises ValueError and keeps state unchanged"""
    data_store, patient, practitioner, appointment_service = foundation()
    completed = Appointment(
        'A1',
        patient,
        practitioner,
        datetime(2026, 10, 1, 9),
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert completed.status is AppointmentStatus.COMPLETED
    assert data_store.list_appointments() == [completed]

def test_cancel_unknown_id() -> None:
    """Unknown appointment ID: a valid but unstored ID raises LookupError"""
    _, _, _, appointment_service = foundation()
    with pytest.raises(LookupError):
        appointment_service.cancel_appointment('A2')

def test_cancel_invalid_id() -> None:
    """Invalid aapointment ID: blank or non-string IDs raise ValueError"""
    _, _, _, appointment_service = foundation()
    for invalid_id in ['', ' ', None, 1]:
        with pytest.raises(ValueError):
            appointment_service.cancel_appointment(invalid_id)

# ------------------------------------
#       Stage 7 extended tests
# ------------------------------------

# ----- Registration (FR-01) -----

def test_register_patient_stores_valid_data() -> None:
    """Valid registration: an unused patient ID is stored and can be found again"""
    data_store, _, _, _ = foundation()
    registered = PatientService(data_store).register_patient('P2', 'Sam Example')
    assert data_store.find_patient('P2') is registered
    assert registered.name == 'Sam Example'

def test_duplicate_patient_id_with_spaces_is_rejected() -> None:
    """Trimmed duplicate ID: ' P1 ' counts as P1, raises ValueError and keeps the original"""
    data_store, patient, _, _ = foundation()
    with pytest.raises(ValueError):
        PatientService(data_store).register_patient(' P1 ', 'Replacement')
    assert data_store.find_patient('P1') is patient
    assert patient.name == 'Alex Example'
    assert data_store.list_patients() == [patient]

def test_patient_registration_is_case_sensitive() -> None:
    """Case-sensitive IDs: p1 is a different patient from P1, so both are stored"""
    data_store, patient, _, _ = foundation()
    lowercase = PatientService(data_store).register_patient('p1', 'Lowercase Example')
    assert lowercase is not patient
    assert data_store.find_patient('p1') is lowercase
    assert data_store.find_patient('P1') is patient

def test_same_id_allowed_for_patient_and_practitioner() -> None:
    """Unique per entity type: a practitioner can use an ID a patient already has"""
    data_store, patient, _, _ = foundation()
    practitioner = PractitionerService(data_store).register_practitioner(
        'P1',
        'Morgan Example',
        'General',
    )
    assert data_store.find_practitioner('P1') is practitioner
    assert data_store.find_patient('P1') is patient

# ----- Booking and conflicts (FR-04, FR-05) -----

def test_book_appointment_trims_participant_ids() -> None:
    """Booking and lookup: spaces around IDs still find the registered objects"""
    _, patient, practitioner, appointment_service = foundation()
    appointment = appointment_service.book_appointment(
        'A1',
        ' P1 ',
        ' D1 ',
        datetime(2026, 10, 1, 9),
    )
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment_service.find_appointment(' A1 ') is appointment

def test_book_unknown_practitioner_rejected() -> None:
    """Unknown practitioner: raises LookupError and nothing is stored"""
    data_store, _, _, appointment_service = foundation()
    with pytest.raises(LookupError):
        appointment_service.book_appointment(
            'A1',
            'P1',
            'D9',
            datetime(2026, 10, 1, 9),
        )
    assert data_store.list_appointments() == []

def test_conflict_rejected_and_store_unchanged() -> None:
    """Practitioner conflict: same practitioner and time raises ValueError, store unchanged"""
    data_store, _, _, appointment_service = foundation()
    when = datetime(2026, 10, 1, 9)
    original = appointment_service.book_appointment('A1', 'P1', 'D1', when)
    with pytest.raises(ValueError):
        appointment_service.book_appointment('A2', 'P1', 'D1', when)
    assert data_store.list_appointments() == [original]

def test_booking_one_minute_later_is_allowed() -> None:
    """Conflict boundary: same practitioner one minute later is not a conflict"""
    data_store, _, _, appointment_service = foundation()
    first = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9),
    )
    second = appointment_service.book_appointment(
        'A2',
        'P1',
        'D1',
        datetime(2026, 10, 1, 9, 1),
    )
    assert second.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [first, second]

def test_cancelled_booking_frees_slot() -> None:
    """Cancelled slot: a cancelled booking no longer blocks the same practitioner and time"""
    data_store, _, _, appointment_service = foundation()
    when = datetime(2026, 10, 1, 9)
    first = appointment_service.book_appointment('A1', 'P1', 'D1', when)
    appointment_service.cancel_appointment('A1')
    second = appointment_service.book_appointment('A2', 'P1', 'D1', when)
    assert first.status is AppointmentStatus.CANCELLED
    assert second.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [first, second]