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