"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime

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


def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


# ----- Stage 9 interactive menu -----

LINE = '-' * 60
BANNER = '=' * 60
MENU_LINES = (
    '[1] Register patient',
    '[2] Find patient',
    '[3] Register practitioner',
    '[4] Find practitioner',
    '[5] Book appointment',
    '[6] Cancel appointment',
    '[7] Find appointment',
    '[8] List practitioner appointments',
    '[0] Exit',
)


def parse_status(text: str) -> AppointmentStatus | None:
    """Convert console status text to an enum; blank means all statuses.

    Raise ValueError for any other text.
    """
    text = text.strip().lower()
    if not text:
        return None
    for status in AppointmentStatus:
        if status.value == text:
            return status
    raise ValueError('Status must be scheduled, cancelled or completed')


def status_label(status: AppointmentStatus) -> str:
    """Return a display label such as 'Scheduled'."""
    return status.value.capitalize()


def show_patient(patient: Patient, output) -> None:
    """Display patient details."""
    output(f'   Patient ID : {patient.patient_id}')
    output(f'   Name       : {patient.name}')


def show_practitioner(practitioner: Practitioner, output) -> None:
    """Display practitioner details."""
    output(f'   Practitioner ID : {practitioner.practitioner_id}')
    output(f'   Name            : {practitioner.name}')
    output(f'   Specialty       : {practitioner.specialty}')


def show_appointment(appointment: Appointment, output) -> None:
    """Display appointment details, reusing format_appointment."""
    patient = appointment.patient
    practitioner = appointment.practitioner
    output(f'   Appointment ID : {appointment.appointment_id}')
    output(f'   Patient        : {patient.name} ({patient.patient_id})')
    output(
        f'   Practitioner   : {practitioner.name} '
        f'({practitioner.practitioner_id})',
    )
    output(f'   Specialty      : {practitioner.specialty}')
    output(f'   Date/time      : {appointment.date_time:%Y-%m-%d %H:%M}')
    output(f'   Status         : {status_label(appointment.status)}')
    output(f'   Reference      : {format_appointment(appointment)}')


def register_patient(services, input_func, output) -> None:
    """Menu 1: register a patient."""
    patient = services['patients'].register_patient(
        input_func('Patient ID: '),
        input_func('Patient name: '),
    )
    output('Patient registered successfully.')
    show_patient(patient, output)


def find_patient(services, input_func, output) -> None:
    """Menu 2: find a patient by ID."""
    patient = services['patients'].find_patient(input_func('Patient ID: '))
    output(f'Patient found. {patient.patient_id}: {patient.name}')
    show_patient(patient, output)


def register_practitioner(services, input_func, output) -> None:
    """Menu 3: register a practitioner."""
    practitioner = services['practitioners'].register_practitioner(
        input_func('Practitioner ID: '),
        input_func('Practitioner name: '),
        input_func('Specialty: '),
    )
    output('Practitioner registered successfully.')
    show_practitioner(practitioner, output)


def find_practitioner(services, input_func, output) -> None:
    """Menu 4: find a practitioner by ID."""
    practitioner = services['practitioners'].find_practitioner(
        input_func('Practitioner ID: '),
    )
    output(
        f'Practitioner found. {practitioner.practitioner_id}: '
        f'{practitioner.name}, {practitioner.specialty}',
    )
    show_practitioner(practitioner, output)


def book_appointment(services, input_func, output) -> None:
    """Menu 5: book using IDs and a parsed date/time."""
    appointment_id = input_func('Appointment ID: ')
    patient_id = input_func('Patient ID: ')
    practitioner_id = input_func('Practitioner ID: ')
    date_time = parse_date_time(
        input_func('Date/time [YYYY-MM-DD HH:MM]: ').strip(),
    )
    appointment = services['appointments'].book_appointment(
        appointment_id,
        patient_id,
        practitioner_id,
        date_time,
    )
    output('Appointment booked successfully.')
    show_appointment(appointment, output)


def cancel_appointment(services, input_func, output) -> None:
    """Menu 6: cancel an appointment; the record is retained."""
    appointment = services['appointments'].cancel_appointment(
        input_func('Appointment ID: '),
    )
    output('Appointment cancelled successfully.')
    show_appointment(appointment, output)


def find_appointment(services, input_func, output) -> None:
    """Menu 7: find an appointment, including cancelled ones."""
    appointment = services['appointments'].find_appointment(
        input_func('Appointment ID: '),
    )
    output('Appointment found.')
    show_appointment(appointment, output)


def list_appointments(services, input_func, output) -> None:
    """Menu 8: list a practitioner's appointments; blank status = all."""
    practitioner_id = input_func('Practitioner ID: ')
    status = parse_status(input_func(
        'Status filter [scheduled/cancelled/completed, blank = all]: ',
    ))
    results = services['appointments'].list_practitioner_appointments(
        practitioner_id,
        status,
    )
    practitioner = services['practitioners'].find_practitioner(
        practitioner_id,
    )
    output(
        f'Appointments for {practitioner.name} '
        f'({practitioner.practitioner_id})',
    )
    if status is None:
        output('Filter: All statuses')
    else:
        output(f'Filter: {status_label(status)}')
    output(LINE)
    if not results:
        output('No appointments found.')
        return
    for number, appointment in enumerate(results, start=1):
        output('')
        output(f'{number}. {appointment.appointment_id}')
        output(
            f'   Patient   : {appointment.patient.name} '
            f'({appointment.patient.patient_id})',
        )
        output(f'   Date/time : {appointment.date_time:%Y-%m-%d %H:%M}')
        output(f'   Status    : {status_label(appointment.status)}')
        output(f'   Reference : {format_appointment(appointment)}')
    output('')
    output(LINE)
    noun = 'appointment' if len(results) == 1 else 'appointments'
    output(f'{len(results)} {noun} found.')


MENU_ACTIONS = {
    '1': register_patient,
    '2': find_patient,
    '3': register_practitioner,
    '4': find_practitioner,
    '5': book_appointment,
    '6': cancel_appointment,
    '7': find_appointment,
    '8': list_appointments,
}


def show_menu(output) -> None:
    """Display the main menu."""
    output('')
    output('MAIN MENU')
    output(LINE)
    for line in MENU_LINES:
        output(line)
    output(LINE)


def run_menu(input_func=input, output=print) -> None:
    """Stage 9: run the register/find/book/cancel/list/exit menu.

    One data store and one set of services are used for the whole
    session. Expected ValueError and LookupError messages are shown and
    the menu continues. Data is discarded on exit.
    """
    data_store = SmartCareDataStore()
    services = {
        'patients': PatientService(data_store),
        'practitioners': PractitionerService(data_store),
        'appointments': AppointmentService(data_store),
    }

    output(BANNER)
    output('SMARTCARE'.center(60))
    output('Interactive Console'.center(60))
    output(BANNER)
    output('Session data is temporary and will be discarded when you exit.')

    while True:
        show_menu(output)
        try:
            choice = input_func('Select an option: ').strip()
            output('')
            if choice == '0':
                break
            action = MENU_ACTIONS.get(choice)
            if action is None:
                output('Unknown choice. Choose a number from 0 to 8.')
            else:
                action(services, input_func, output)
        except EOFError:
            output('')
            break
        except (ValueError, LookupError) as error:
            output(f'Error: {error}')
    output('Goodbye. Session data discarded.')