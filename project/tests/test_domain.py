"""Stage 7 checks for Patient, Practitioner and Appointment on their own."""

from datetime import datetime

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)

# ------------------------------------
#       Using tests from Part C
# ------------------------------------

# ----- Patient -----

def test_patient_stores_valid_fields() -> None:
    """Valid patient: the ID and name are stored as given"""
    patient = Patient('P1', 'Alex Example')
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'

def test_patient_trims_id() -> None:
    """Trimmed IDs: spaces around the ID are ignored"""
    patient = Patient(' P1 ', 'Alex Example')
    assert patient.patient_id == 'P1'

def test_blank_patient_id() -> None:
    """Blank patient ID: blank or non-string IDs raise ValueError"""
    for invalid_id in ['', ' ', None]:
        with pytest.raises(ValueError):
            Patient(invalid_id, 'Alex Example')

def test_blank_patient_name() -> None:
    """Blank patient name: blank or non-string names raise ValueError"""
    for invalid_name in ['', ' ', None]:
        with pytest.raises(ValueError):
            Patient('P1', invalid_name)

# ----- Practitioner -----

def test_practitioner_stores_valid_fields() -> None:
    """Valid Practitioner: the ID and name are stored as given"""
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General'

def test_practitioner_trims_id() -> None:
    """Trimmed IDs: spaces around the ID are ignored"""
    practitioner = Practitioner(' D1 ', 'Taylor Example', 'General')
    assert practitioner.practitioner_id == 'D1'

def test_blank_practitioner_fields() -> None:
    """Blank practitioner fields: blank or non-string IDs, names, and specialty raise ValueErrors"""
    for invalid_field in ['', ' ', None]:
        with pytest.raises(ValueError):
            Practitioner(invalid_field, 'Taylor Example', 'General')
        with pytest.raises(ValueError):
            Practitioner('D1', invalid_field, 'General')
        with pytest.raises(ValueError):
            Practitioner('D1', 'Taylor Example', invalid_field)

# ----- Appointment -----

def test_appointment_begins_scheduled() -> None:
    """New appointment: stores participants, time, and starts as SCHEDULED"""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    when = datetime(2026, 10, 1, 9)
    appointment = Appointment('A1', patient, practitioner, when)
    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == when
    assert appointment.status is AppointmentStatus.SCHEDULED

def test_cancel_changes_status() -> None:
    """Cancellation: cancelling a SCHEDULED appointment changes the status to CANCELLED"""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    appointment = Appointment('A1', patient, practitioner, datetime(2026, 10, 1, 9))
    appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED

def test_cancelled_twice_rejects() -> None:
    """Repeated cancellation: raises ValueError and stays CANCELLED"""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    appointment = Appointment('A1', patient, practitioner, datetime(2026, 10, 1, 9))
    appointment.cancel()
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED

def test_cancel_from_completed_rejects() -> None:
    """Cancellation from COMPLETED: raises ValueError and rejects"""
    patient = Patient('P1', 'Alex Example')
    practitioner = Practitioner('D1', 'Taylor Example', 'General')
    appointment = Appointment('A1', patient, practitioner, datetime(2026, 10, 1, 9), AppointmentStatus.COMPLETED)
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.COMPLETED

def test_appointment_rejects_invalid_fields() -> None:
     """Invalid Fields: a blank ID, wrong patient/practitioner data types, wrong status, or invalid date/time raises a ValueError"""
     patient = Patient('P1', 'Alex Example')
     practitioner = Practitioner('D1', 'Taylor Example', 'General')
     when = datetime(2026, 10, 1, 9)
     with pytest.raises(ValueError):
          Appointment('', patient, practitioner, when)
     with pytest.raises(ValueError):
            Appointment('A1', 'P1', practitioner, when)
     with pytest.raises(ValueError):
            Appointment('A1', patient, 'D1', when)
     with pytest.raises(ValueError):
            Appointment('A1', patient, practitioner, datetime(2026, 10, 1, 9, 0, 30))
     with pytest.raises(ValueError):
            Appointment('A1', patient, practitioner, when, 'scheduled')
