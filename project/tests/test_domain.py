"""Tests for SmartCare domain objects (domain.py)."""

import pytest
from datetime import datetime
from smartcare.domain import (
    Patient,
    Practitioner,
    Appointment,
    AppointmentStatus,
    required_text,
    validate_date_time,
)


# --- Helpers for required_text ---

class TestRequiredText:
    def test_strips_whitespace(self):
        result = required_text("  Alice  ", "Name")
        assert result == "Alice"

    def test_rejects_blank(self):
        with pytest.raises(ValueError, match="cannot be blank"):
            required_text("", "Name")

    def test_rejects_none(self):
        with pytest.raises(ValueError, match="cannot be blank"):
            required_text(None, "Name")

    def test_rejects_whitespace_only(self):
        with pytest.raises(ValueError, match="cannot be blank"):
            required_text("   ", "Name")


# --- Helpers for validate_date_time ---

class TestValidateDateTime:
    def test_accepts_naive_minute_precision(self):
        dt = datetime(2025, 6, 15, 10, 30)
        result = validate_date_time(dt)
        assert result is dt

    def test_rejects_timezone_aware(self):
        from datetime import timezone, timedelta
        tz = timezone(timedelta(hours=1))
        dt = datetime(2025, 6, 15, 10, 30, tzinfo=tz)
        with pytest.raises(ValueError, match="local date/time"):
            validate_date_time(dt)

    def test_rejects_with_seconds(self):
        dt = datetime(2025, 6, 15, 10, 30, 15)
        with pytest.raises(ValueError, match="minute precision"):
            validate_date_time(dt)

    def test_rejects_with_microseconds(self):
        dt = datetime(2025, 6, 15, 10, 30, microsecond=123)
        with pytest.raises(ValueError, match="minute precision"):
            validate_date_time(dt)

    def test_rejects_non_datetime(self):
        with pytest.raises(ValueError, match="must be a datetime value"):
            validate_date_time("2025-06-15")


# --- Patient ---

class TestPatient:
    def test_constructs_with_valid_data(self):
        p = Patient("P1", "Alice Smith")
        assert p.patient_id == "P1"
        assert p.name == "Alice Smith"

    def test_strips_name(self):
        p = Patient("P1", "  Alice Smith  ")
        assert p.name == "Alice Smith"

    def test_rejects_blank_id(self):
        with pytest.raises(ValueError, match="Patient ID"):
            Patient("", "Alice")

    def test_rejects_blank_name(self):
        with pytest.raises(ValueError, match="Patient name"):
            Patient("P1", "")

    def test_id_is_read_only(self):
        p = Patient("P1", "Alice")
        with pytest.raises(AttributeError):
            p.patient_id = "P2"


# --- Practitioner ---

class TestPractitioner:
    def test_constructs_with_valid_data(self):
        pr = Practitioner("Dr1", "Dr. Bob", "Cardiology")
        assert pr.practitioner_id == "Dr1"
        assert pr.name == "Dr. Bob"
        assert pr.specialty == "Cardiology"

    def test_strips_all_fields(self):
        pr = Practitioner("  Dr1  ", "  Dr. Bob  ", "  Cardiology  ")
        assert pr.practitioner_id == "Dr1"
        assert pr.name == "Dr. Bob"
        assert pr.specialty == "Cardiology"

    def test_rejects_blank_id(self):
        with pytest.raises(ValueError, match="Practitioner ID"):
            Practitioner("", "Bob", "Cardiology")

    def test_rejects_blank_name(self):
        with pytest.raises(ValueError, match="Practitioner name"):
            Practitioner("Dr1", "", "Cardiology")

    def test_rejects_blank_specialty(self):
        with pytest.raises(ValueError, match="Specialty"):
            Practitioner("Dr1", "Bob", "")


# --- Appointment ---

class TestAppointment:
    def setup_method(self):
        self.patient = Patient("P1", "Alice")
        self.practitioner = Practitioner("Dr1", "Dr. Bob", "Cardiology")
        self.datetime = datetime(2025, 6, 15, 10, 30)

    def test_constructs_with_valid_data_default_status(self):
        appt = Appointment("A1", self.patient, self.practitioner, self.datetime)
        assert appt.appointment_id == "A1"
        assert appt.patient is self.patient
        assert appt.practitioner is self.practitioner
        assert appt.date_time == self.datetime
        assert appt.status == AppointmentStatus.SCHEDULED

    def test_constructs_with_custom_status(self):
        appt = Appointment(
            "A1", self.patient, self.practitioner, self.datetime,
            status=AppointmentStatus.COMPLETED,
        )
        assert appt.status == AppointmentStatus.COMPLETED

    def test_rejects_invalid_status_type(self):
        with pytest.raises(ValueError, match="Invalid appointment status"):
            Appointment("A1", self.patient, self.practitioner, self.datetime,
                        status="scheduled")

    def test_rejects_non_patient_object(self):
        with pytest.raises(ValueError, match="requires a Patient object"):
            Appointment("A1", "not_a_patient", self.practitioner, self.datetime)

    def test_rejects_non_practitioner_object(self):
        with pytest.raises(ValueError, match="requires a Practitioner object"):
            Appointment("A1", self.patient, "not_a_practitioner", self.datetime)

    def test_rejects_blank_id(self):
        with pytest.raises(ValueError, match="Appointment ID"):
            Appointment("", self.patient, self.practitioner, self.datetime)

    def test_rejects_tz_aware_datetime(self):
        from datetime import timezone, timedelta
        tz = timezone(timedelta(hours=1))
        dt = datetime(2025, 6, 15, 10, 30, tzinfo=tz)
        with pytest.raises(ValueError, match="local date/time"):
            Appointment("A1", self.patient, self.practitioner, dt)

    def test_rejects_datetime_with_seconds(self):
        dt = datetime(2025, 6, 15, 10, 30, 15)
        with pytest.raises(ValueError, match="minute precision"):
            Appointment("A1", self.patient, self.practitioner, dt)

    def test_properties_are_readonly(self):
        appt = Appointment("A1", self.patient, self.practitioner, self.datetime)
        with pytest.raises(AttributeError):
            appt.appointment_id = "A2"
        with pytest.raises(AttributeError):
            appt.patient = Patient("P2", "Bob")
        with pytest.raises(AttributeError):
            appt.practitioner = Practitioner("Dr2", "Bob", "Dental")
        with pytest.raises(AttributeError):
            appt.date_time = datetime(2025, 7, 1, 11, 0)

    # --- Cancel transitions ---

    def test_cancel_scheduled_to_cancelled(self):
        appt = Appointment("A1", self.patient, self.practitioner, self.datetime)
        assert appt.status == AppointmentStatus.SCHEDULED
        appt.cancel()
        assert appt.status == AppointmentStatus.CANCELLED

    def test_cancel_already_cancelled_raises(self):
        appt = Appointment("A1", self.patient, self.practitioner, self.datetime)
        appt.cancel()
        with pytest.raises(ValueError, match="Only SCHEDULED"):
            appt.cancel()

    def test_cancel_completed_raises(self):
        appt = Appointment(
            "A1", self.patient, self.practitioner, self.datetime,
            status=AppointmentStatus.COMPLETED,
        )
        with pytest.raises(ValueError, match="Only SCHEDULED"):
            appt.cancel()

    def test_cancel_does_not_change_other_fields(self):
        appt = Appointment("A1", self.patient, self.practitioner, self.datetime)
        appt.cancel()
        assert appt.appointment_id == "A1"
        assert appt.patient is self.patient
        assert appt.practitioner is self.practitioner
        assert appt.date_time == self.datetime