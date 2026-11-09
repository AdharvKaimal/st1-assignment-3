# Stage 7 Testing and Verification Record

Group/tutorial: Tuesday Group 4 (13:30-15:30)  
Members/cohorts: (GitHub) AdharvKaimal, krestianreyes13, jesshall902
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Submit registration form with valid details (name, DOB, contact, ID). | Submit form with missing mandatory fields (e.g., blank name or invalid email format). | Patient record is created in the database with unique ID and all provided details are stored accurately. |
| FR-05 Prevent practitioner conflict | Book two different patients with the same practitioner for different time slots. |Attempt to book two patients with the same practitioner for overlapping time slots. | System rejects the second booking and displays a "Time Conflict" error; practitioner schedule remains unchanged. |
| FR-06 Cancel appointment | Click "Cancel" on an upcoming appointment and confirm.
 | Attempt to cancel an appointment that has already started or ended. | Appointment status changes to "Cancelled"; patient and practitioner are notified; appointment is removed from active calendar. |
| FR-07 Retain cancelled history | Cancel an appointment and then view the "Appointment History" log. | Attempt to delete a cancelled appointment from the history log. | Cancelled appointment remains in the history with status "Cancelled" and timestamp; full audit trail is preserved. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: The assertion is a tautology, and therefore always passes regardless of system state or logic. It does not test actual behaviour, limits or data integrity, and so it is useless for testing requirements.

`assert appointment is not None`
Judgement: Weak/unclear  Why: This only checks that an object was returned, not that it is valid or correct. It fails to verify critical behaviour like whether the correct appointment was retrieved, if the status is valid, or if the data matches expectations. It does not define functional limits.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: This explicitly verifies the core state change required by FR-06 and FR-07. It confirms the specific intended behaviour (status update) and implicitly limits the scope to the appointment object's status field, ensuring no other side effects are assumed. 

`assert len(results) > 0`
Judgement: Weak/unclear  Why:  This only confirms that some results exists, not that they are the correct results. It fails to verify behaviour against specific crtieria (such as filtering by patient ID or date). It does not define limits on data accuracy or completeness.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: This verifies data persistence and identity consistency (FR-07). It confirms that the specific appointmnet object remains retrievable and unchanged in the store after operations, effectively testing the "retain history" requirement with precise limits on object identity.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 
Here are the boundary and edge cases for the specified scenarios in the SmartCare system:

| Input / State | Expected Result | Supporting Contract |
|---|---|---|
| Blank Identifier (e.g., patientId = "" or null) | Registration fails; error message: "Identifier is required." No record is created. | Precondition: identifier != null and identifier.trim().length > 0. Invariant: All entities must have a unique, non-empty ID. |
| Whitespace-Only Name (e.g., name = "   " or " \t ") | Registration fails; error message: "Name cannot contain only whitespace." No record is created. | Precondition: name must contain at least one non-whitespace character. Sanitisation: name.trim() is used for storage, but raw input is validated first. |
| Same-Time Practitioner Bookings (Two patients, same practitioner, same time slot) | Second booking fails; error message: "Practitioner is already booked at this time." | Constraint: PractitionerSchedule must enforce mutual exclusivity for overlapping time intervals. Logic: start_time < existing_end AND end_time > existing_start must be false for concurrency. |
| Cancelled Appointment (Attempting to cancel an already cancelled appointment) | System ignores the request or returns a warning: "Appointment is already cancelled." No status change or double-notification. | Idempotency: The cancel operation must be idempotent.
State Machine: Transition CANCELLED -> CANCELLED is invalid or no-op. |
| Invalid Status Transition (e.g., moving from CANCELLED directly to COMPLETED or SCHEDULED) | Transition rejected; error message: "Invalid status transition from (Current) to (Target)." | State Transition Table: Only allowed transitions are defined (e.g., SCHEDULED -> CANCELLED, SCHEDULED -> COMPLETED). Invariant: The system must always be in a valid state. |

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Asserting "is not None" only proves an object was instantiated, not that it is valid or correct. It fails to verify business rules (e.g., correct data, status, or constraints). | Verify that the created patient object has all required fields populated correctly and that the database returns the exact same record when queried by ID. |
| 2 | Same as Candidate 1: is not None is a weak assertion. It provides no verification of state integrity, data accuracy, or successful persistence in the system. | Verify that the practitioner’s schedule reflects the new booking slot and that no other practitioner is double-booked in that time interval. |
| 3 | "assert True" is a tautology; it always passes regardless of system state. It performs no actual testing, offering zero coverage of logic, data, or behavior. | Verify that the appointment status transitions to 'CANCELLED' in the database and that the practitioner’s calendar updates to reflect the cancellation. |
| 4 | Assuming SMS notifications exist without mocking or verifying the notification service. If SMS is disabled or misconfigured, the test may hang, fail externally, or silently ignore delivery, breaking isolation. | Verify that a notification event is triggered for the cancellation. Mock the SMS service to assert that the correct message payload is passed to the notification handler. |
| 5 | Same as Candidate 4: Tightly coupling the test to a specific external I/O implementation (SMS). This makes the test brittle and dependent on external infrastructure rather than internal logic. | Verify that the system logs a cancellation record for audit purposes. Ensure the history log contains the appointment ID, cancellation timestamp, and user who performed the action. |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
Coverage only shows which lines ran, not whether the tests check the right thing. A test that calls cancel_appointment but only asserts True would give full coverage and still prove nothing about the status, the returned object or rejected input.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 | AC-01.1 | TC-FR01-01 | Positive / Integration | test_register_patient_valid_new_id (awaiting implementation) | Valid required patient data with an unused ID is stored and retrievable via lookup. | Supplied evidence: partial domain only; constructor-only test does not prove storage; needs DB round-trip. | student-authoured | 
| FR-01	| AC-01.2 | TC-FR01-02 | Negative | test_register_patient_duplicate_id_rejected (awaiting implementation) | Registration with an existing patient ID is rejected; no second record created. | Student-authoured: awaiting implementation. | student-authoured |
| FR-01 | Supporting contract (no canonical AC): "Patient identifier must be non-blank after trimming" under FR-01 | TC-FR01-03 | Negative / Boundary | test_register_patient_blank_identifier_rejected (awaiting implementation) | Blank or whitespace-only identifier is rejected with a validation error; not treated as AC-01.2 duplicate rejection. | Student-authoured: awaiting implementation. | student-authoured |
| FR-02 | AC-02.1 / AC-02.2 | TC-FR02-01 | Positive + Negative | test_lookup_known_and_unknown_patient (awaiting implementation) | Known patient lookup succeeds and returns the record; unknown patient lookup reports absence (e.g., None/not-found). | Student-authoured: awaiting implementation. | student-authoured |
| FR-03 | Practitioner registration (FR-03 scope); practitioner lookup is a supporting operation over registered objects |	TC-FR03-01 | Positive | test_register_practitioner_valid (awaiting implementation) | A valid practitioner with a unique ID is registered and available for subsequent booking operations. | Student-authoured: awaiting implementation. | student-authoured |
| FR-04 | AC-03.1 | TC-FR04-01 | Positive / Integration | test_book_appointment_succeeds (awaiting implementation) | Registered participants, a unique ID and a free time produce a stored SCHEDULED appointment. | Supplied evidence: partial domain only; object construction alone insufficient; requires store persistence check. | student-authoured | 
| FR-04 | AC-03.2 | TC-FR04-02 | Negative | test_book_unknown_participant_rejected (awaiting implementation) | Booking referencing an unknown patient or unknown practitioner is rejected; no appointment persisted. | Student-authoured: awaiting implementation. | student-authoured | 
| FR-05 | AC-04.1 / AC-04.2 | TC-FR05-01 | Negative + Positive | test_practitioner_conflict_blocks_same_slot_other_practitioner_allowed (awaiting implementation) | Same practitioner/exact time/SCHEDULED conflicts (rejected); another practitioner at the same time is allowed. | Student-authoured: awaiting implementation. | student-authoured | 
| FR-06 | AC-05.1 | TC-FR06-01 | Positive | test_cancel_scheduled_appointment (awaiting implementation)	| Cancelling a SCHEDULED appointment changes its status to CANCELLED. | Student-authoured: awaiting implementation. | student-authoured |
| FR-06 | AC-05.3 | TC-FR06-02 | Negative / State transition | test_repeat_cancellation_rejected (awaiting implementation) | Repeated cancellation of an already-CANCELLED appointment is rejected. | Student-authoured: awaiting implementation. | student-authoured |
| FR-07 | AC-05.2 | TC-FR07-01 | Positive / Retrieval | test_cancelled_history_retrievable_in_session (awaiting implmentation) |  Cancelled history remains retrievable in the current session.	| Student-authoured: awaiting implementation. | student-authoured |
| FR-08 | AC-06.1 | TC-FR08-01 | Positive | test_find_appointment_by_known_id (awaiting implementation) | A known appointment ID returns that exact appointment. | Student-authoured: awaiting implementation. | student-authoured |


## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TC-FR01-01 | FR-01 | AC-01.1 | Positive | test_register_patient_stores_valid_data() | Patient record persists in store; lookup by new ID returns the exact registered data. | Supplied tests only asserted object construction (is not None). This proves end-to-end storage and retrieval, satisfying the "stored" clause of AC-01.1. | 
| TC-FR01-02 | FR-01 | AC-01.2 | Negative | test_duplicate_patient_id_is_rejected() | System raises/returns a duplicate-ID error; no second record is created; original record unchanged. | Supplied tests never exercised collision handling. Adds coverage of the uniqueness constraint invariant. |
| TC-FR01-03 | FR-01 | Supporting contract: identifier must be non-blank after trimming (revision 2) | Boundary	test_blank_patient_id_is_rejected()	Whitespace-only or empty ID triggers validation error before persistence; distinct from duplicate-ID error. | Blank-ID validation has no canonical AC; this quotes the precise public contract under FR-01 rather than mislabeling it as AC-01.2. Supplies boundary evidence (empty vs. whitespace variants). |
| TC-FR02-01 | FR-02 | AC-02.1 / AC-02.2 | Positive + Negative | test_lookup_known_and_unknown_patient_reports_correctly() | Known ID returns the patient object; unknown ID reports absence (e.g., None/not-found), not an exception or wrong record. | Supplied tests lacked any lookup verification. Confirms both halves of the paired AC in one controlled scenario. |
| TC-FR03-01 | FR-03 | Practitioner registration scope (lookup = supporting operation) | Positive | test_register_practitioner_makes_it_bookable() | Valid practitioner with unique ID is registered and subsequently resolvable for booking. | Establishes the prerequisite state other FRs depend on; supplied tests assumed practitioners existed without proving registration. | 
| TC-FR04-01 | FR-04 | AC-03.1 | Positive | test_booking_free_slot_creates_scheduled_appointment() | Registered participants + unique ID + free time yield a stored appointment with status SCHEDULED. | Supplied test stopped at object creation. This verifies persistence and the specific initial status value. | 
| TC-FR04-02 | FR-04 | AC-03.2 | Negative | test_booking_unknown_participant_is_rejected() | Booking with unknown patient or practitioner fails; nothing is persisted. | Adds referential-integrity evidence; supplied tests used only valid fixtures. | 
| TC-FR05-01 | FR-05 | AC-04.1 / AC-04.2 | Negative + Positive | test_same_practitioner_exact_time_conflicts_other_practitioner_allowed() | Same practitioner/exact time/SCHEDULED → rejected; different practitioner same time → accepted. | Supplied tests had no concurrency/conflict logic. Proves both the block and the permitted case, preventing over-restrictive implementations. |
| TC-FR06-01 | FR-06 | AC-05.1 | Positive | test_cancel_changes_status() | SCHEDULED appointment transitions to CANCELLED in the store.	| Replaces the useless assert True with a concrete state-transition assertion tied to AC-05.1. | 
| TC-FR06-02 | FR-06 | AC-05.3 | Negative | test_repeat_cancellation_is_rejected() | Second cancel attempt on a CANCELLED appointment is rejected; status remains CANCELLED. | Supplies invalid-state-transition evidence absent from all supplied tests. | 
| TC-FR07-01 | FR-07 | AC-05.2 | Positive | test_cancelled_appointment_remains_retrievable_in_session() | After cancellation, history lookup still returns the appointment with status CANCELLED. | Proves retention/persistence of cancelled records, not just the status flag change. |
| TC-FR08-01 | FR-08 | AC-06.1 | Positive | test_find_appointment_by_known_id_returns_that_appointment() | Known appointment ID resolves to that exact appointment object/data. | Verifies identity/correctness of retrieval rather than mere non-nullity. |


## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TC-FR01-01 | Create Patient(name="A", id="P1"); call store.add(patient). | result = store.lookup("P1"). | assert result is not None and result.name == "A". | Proves storage and retrieval (AC-01.1), not just object creation. | 
| TC-FR01-02 | Call store.add(Patient(id="P1")) once. | Call store.add(Patient(id="P1")) again. | assert len(store.lookup_all()) == 1. | Proves uniqueness constraint (AC-01.2); no duplicate record persisted. |
| TC-FR01-03 | Prepare patient data with id="" or id="   ". | Call store.add(...). | with pytest.raises(ValidationError): ... | Proves blank-ID boundary validation (Supporting Contract); rejects invalid input. | 
| TC-FR02-01 | Register a known patient; ensure unknown ID doesn't exist. | Lookup known ID; Lookup unknown ID. | assert known_result is not None; assert unknown_result is None. | Proves correct lookup for both success and absence (AC-02.1/02.2). |
| TC-FR03-01 | Create Practitioner(id="Dr1"). | Call practitioner_store.add(...). | assert practitioner_store.lookup("Dr1") is not None. | Proves practitioner registration prerequisite for booking (FR-03). | 
| TC-FR04-01 | Register patient and practitioner; define free time slot. | Call booking_service.schedule(patient_id, practitioner_id, slot). | assert appointment.status == AppointmentStatus.SCHEDULED. | Proves successful booking and status assignment (AC-03.1). |
| TC-FR04-02 | Define time slot; use unregistered patient ID. | Call booking_service.schedule(...).	with pytest.raises(ValueError) |  Proves referential integrity rejection (AC-03.2). |
| TC-FR05-01 | Book Practitioner A for 10:00. | Attempt to book Practitioner A for 10:00; Book Practitioner B for 10:00. | with pytest.raises(ConflictError): ...; assert B_booked. | Proves conflict detection and allowance of others (AC-04.1/04.2). | 
| TC-FR06-01 | Create SCHEDULED appointment. | Call booking_service.cancel(appointment_id). | assert appointment.status == AppointmentStatus.CANCELLED.	Proves status transition behavior (AC-05.1). | 
| TC-FR06-02 | Create and cancel an appointment (status = CANCELLED). | Call booking_service.cancel(appointment_id) again. | with pytest.raises(StateError): ... | Proves idempotency/rejection of repeated cancellation (AC-05.3). | 
| TC-FR07-01 | Cancel an appointment. | Call history_store.lookup(appointment_id). | assert result.status == AppointmentStatus.CANCELLED. | Proves history retention (AC-05.2). |
| TC-FR08-01 | Create and store an appointment with ID "A1". | Call booking_service.find("A1"). | assert result.id == "A1". | Proves correct identity retrieval (AC-06.1). |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| TC-FR01-01 | Patient construction with valid data and storage. | awaiting implementation | X |
| TC-FR01-02 | Patient construction with duplicate ID rejection. | awaiting implementation | X |
| TC-FR01-03 | Patient construction with blank/whitespace ID rejection. | awaiting implementation | X |
| TC-FR02-01 | Patient lookup for known vs. unknown ID. | awaiting implementation | X |
| TC-FR03-01 | Practitioner construction with valid data and storage. | awaiting implementation | X |
| TC-FR04-01 | Appointment construction with valid data and initial SCHEDULED status. | awaiting implementation | X |
| TC-FR04-02 | Appointment construction with unknown participant rejection. | awaiting implementation | X |
| TC-FR05-01 | Appointment construction conflict (same practitioner/time) and uniqueness (different practitioner). | awaiting implementation | X |
| TC-FR06-01 | Appointment cancellation (SCHEDULED to CANCELLED). | awaiting implementation | X | 
| TC-FR06-02 | Illegal state transition (CANCELLED to CANCELLED). | awaiting implementation | X | 
| TC-FR07-01 | Appointment cancellation history retention.	| awaiting implementation | X |
| TC-FR08-01 | Appointment retrieval by known ID. | awaiting implementation | X | 

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TC-FR01-01 | Valid registration is stored | FR-01 / AC-01.1 | test_services.py::test_register_patient_stores_valid_data | Passed |
| TC-FR01-02 | Trimmed duplicate patient ID rejected | FR-01 / AC-01.2 | test_services.py::test_duplicate_patient_id_with_spaces_is_rejected | Passed |
| TC-FR01-04 | Case-sensitive IDs, same ID allowed across patient and practitioner | FR-01 / revision 2 contract | test_services.py::test_patient_registration_is_case_sensitive; ::test_same_id_allowed_for_patient_and_practitioner | Passed |
| TC-FR02-01 | Known and unknown patient lookup | FR-02 / AC-02.1, AC-02.2 | test_services.py::test_find_patient_returns_stored_object; ::test_find_patient_unknown_id | Passed |
| TC-FR02-02 | Lookup IDs are trimmed, case-sensitive, and blank/non-string are rejected | FR-02 / revision 2 contract | test_services.py::test_find_patient_trims_ids; ::test_find_patient_is_case_sensitive; ::test_find_patient_invalid_id | Passed |
| TC-FR03-01 | Registered practitioner is found | FR-03 (lookup is a supporting operation) | test_services.py::test_find_practitioner_returns_stored_object | Passed |
| TC-FR04-01 | Booking and appointment lookup with trimmed IDs | FR-04 / AC-03.1; FR-08 / AC-06.1 | test_services.py::test_book_appointment_trims_participant_ids | Passed |
| TC-FR04-02 | Unknown practitioner rejected, nothing stored | FR-04 / AC-03.2 | test_services.py::test_book_unknown_practitioner_rejected | Passed |
| TC-FR05-01 | Practitioner conflict rejected, store unchanged | FR-05 / AC-04.1 | test_services.py::test_conflict_rejected_and_store_unchanged | Passed |
| TC-FR05-02 | Same practitioner one minute later is allowed | FR-05 / AC-04.2 | test_services.py::test_booking_one_minute_later_is_allowed | Passed |
| TC-FR05-03 | Cancelled booking frees the slot | FR-05 / revision 2 contract | test_services.py::test_cancelled_booking_frees_slot | Passed |
| TC-FR06-01 | Cancel returns the same object as CANCELLED | FR-06 / AC-05.1 | test_services.py::test_cancel_same_object_return_cancelled | Passed |
| TC-FR06-02 / 03 | Repeated and COMPLETED cancellation rejected, state unchanged | FR-06 / AC-05.3 | test_services.py::test_cancelled_twice_keeps_state; ::test_cancel_from_completed_keeps_state | Passed |
| TC-FR06-04 | Unknown appointment ID gives LookupError; blank/non-string gives ValueError | FR-06 / revision 2 contract | test_services.py::test_cancel_unknown_id; ::test_cancel_invalid_id | Passed |
| TC-FR07-01 | Cancelled appointment is retained and retrievable | FR-07 / AC-05.2 | test_services.py::test_cancelled_appointment_is_stored | Passed |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Patient registration | Duplicate ID with spaces (' P1 ') | ValueError; original patient unchanged | TC-FR01-02 |
| Patient registration | p1 when P1 already exists | Allowed - two different patients | TC-FR01-04 |
| Practitioner registration | Same ID as an existing patient | Allowed (unique per entity type) | TC-FR01-04 |
| Patient lookup | Blank, space-only, None or 1 | ValueError | TC-FR02-02 |
| Patient lookup | ' P1 ' (spaces) / p1 (wrong case) | ' P1 ' finds P1, p1 raises LookupError | TC-FR02-02 |
| Patient lookup | Valid but unregistered ID | LookupError | TC-FR02-01 |
| Booking | Unknown practitioner | LookupError - list_appointments() empty | TC-FR04-02 |
| Booking | Same practitioner, exact same time as a SCHEDULED appointment | ValueError - store holds only the original | TC-FR05-01 |
| Booking | Same practitioner, one minute later | Allowed | TC-FR05-02 |
| Booking | Same practitioner and time after the first booking was cancelled | Allowed - first stays CANCELLED | TC-FR05-03 |
| Cancellation | Already CANCELLED | ValueError - status stays CANCELLED | TC-FR06-02 |
| Cancellation | COMPLETED | ValueError - status stays COMPLETED | TC-FR06-03 |
| Cancellation | Unknown ID / blank ID | LookupError / ValueError | TC-FR06-04 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-05 Prevent practitioner conflict
Acceptance criterion: AC-04.1 and AC-04.2: Same practitioner, exact time and an existing SCHEDULED appointment conflicts; another practitioner at the same time is allowed.
Behaviour to test: New booking is rejected when the same practitioner already has a SCHEDULED appointment for the same date and time. Different practitioners at the same time are allowed.
Human-first test idea/categories:
- Same practitoner, same time → Rejected.
- Different practitioner, same time → Accepted.
- Same practitioner, one minute later → Accepted.
- Same practitioner and same time, but after cancellation → Accepted.
Prompt and purpose: Used the Stage 7 Copilot prompt to generate candidate tests for FR-05.

For each significant candidate, copy this entry as needed:
**Candidate 1**
- Copilot test idea/candidate: Attempt to create two appointments with the same practitioner and exact same time.
- What it claims to verify: Practitioner conflict checking.
- Requirement trace: FR-05 / AC-04.1
- Assertion quality: Strong.
- Human critique: Verifies required behaviour.
- Decision: Accept
- Reason: Directly checks the required conflict rule.
- Final test reference if accepted/modified: test_services.py::test_conflict_rejected_and_store_unchanged
- Actual verification result: Passed

**Candidate 2**
- Copilot test idea/candidate: Verify a booking succeeds if the practitioner is available one minute later.
- What it claims to verify: Valid non-conflicting booking.
- Requirement trace: FR-05 / AC-04.2
- Assertion quality: Strong.
- Human critique: Matches the SmartCare contract and checks an allowed booking scenario.
- Decision: Accept
- Reason: Verifies that conflict checking is not over-restrictive.
- Final test reference if accepted/modified: test_services.py::test_booking_one_minute_later_is_allowed
- Actual verification result: Passed

**Candidate 3**
- Copilot test idea/candidate: Verify overlapping appointment durations are rejected.
- What it claims to verify: Practitioner conflict checking.
- Requirement trace: None
- Assertion quality: N/A
- Human critique: Duration overlap is not included in SmartCare's requirements (only same date/time restrictions are needed).
- Decision: Reject
- Reason: Out of scope.
- Final test reference if accepted/modified: N/A
- Actual verification result: N/A

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

**Which Copilot-generated test looked convincing but was weak?:** 
Candidate 3 (rejecting overlapping appointment durations). It sounded like a sensible conflict test, but SmartCare only conflicts on the same practitioner at the exact same date and time (out of scope).

**Why was it weak?:**
It tested a rule that wasn't outlined in the requirements.

**How did you strengthen it?:**
I rejected it and kept the tests in scope. 

**Accepted / modified / rejected test decisions and evidence:** Accepted: Candidate 1 (conflict rejection) and Candidate 2 (valid booking 1 minute later). Rejected: Candidate 3 (appointment duration overlap check).

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| python -m pytest | project/ | 8b49c66 | 56 | 0 | | | All tests pass together. Stage 7 extended services tests were not included in this run. |
| python -m pytest | project/ | ad4ffea | 65 | 0 | | | All tests passed together, included extended service tests. |

Individual test runs and changed-order independence evidence: 
- `python -m pytest tests/test_services.py::test_cancelled_booking_frees_slot` → 1 passed in 0.12s
- `python -m pytest tests/test_domain.py::TestPatient::test_rejects_blank_id` → 1 passed in 0.10s
Optional tutor-led demonstration notes: N/A
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: No failures to diagnose. The first run collected 56 tests, which showed the extended service tests still had to be added, and after adding them the suite passed with 65.

## K What the Suite Still Does Not Prove

What does your test suite still not prove?:
- It only covers the cases we wrote, using fixed synthetic data. Other IDs or times could behave differently.
- The domain tests for rejected cancellations check the exception but not that the status is unchanged afterwards.
- Failed lookups aren't shown to leave the stores unchanged.
- It doesn't cover the console, queries or menu, which belong to later stages.
Coverage if used: Not used
Which uncovered areas matter, and why does coverage percentage alone not establish correctness?: Coverage only shows which lines ran, not whether the assertions check the right behaviour, so we didn't use it.
Optional fixtures/parametrisation used and why, if any: Not used.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| Domain Tests | documentation/s6_Adharv | https://github.com/AdharvKaimal/st1-assignment-3/pull/9 | jesshall902 | N/A | 29/10/26 |
| Stage 7 extended service tests | docs/stage6_stage7 | https://github.com/AdharvKaimal/st1-assignment-3/pull/14 | krestianreyes13 | N/A | 9/11/26 |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| jesshall902 | Drafted an initial test_domain.py on feature/stage7-domain-tests - an extended version was later merged via PR #9. Added the Stage 7 extended service tests (9) to test_services.py and helped complete sections F to O for Stage 7's documentation | https://github.com/AdharvKaimal/st1-assignment-3/compare/main...feature/stage7-domain-tests, https://github.com/AdharvKaimal/st1-assignment-3/pull/14 |
| krestianreyes13 | Helped draft, review, and provide feedback on documentation sections (particular F-O), and reviewed the extended test_services.py tests | https://github.com/AdharvKaimal/st1-assignment-3/pull/14 |

## N Formative Questions

1. What question does verification answer?
Verifications ask whether the implementations meet the specificed requirements.

2. What question does validation answer?
Validation asks whether the product meets the intended user need (makes sure it is in scope).

3. What is a unit test?
A unit test checks the behaviour of one small part of code on its own (such as an appointment changing from SCHEDULED to CANCELLED).

4. What is a pytest fixture?
A pytest fixture is a reusable setup function that provides new test data or objects for tests.

5. What is parametrisation in pytest?
Parametrisation allows the same test to run multiple times using different inputs.

6. What is regression testing?
Regression testing is re-running all prior tests after a change to ensure that things that previously worked haven't broken.

7. What does code coverage tell us, and what does it not prove?
Coverage tells us which lines of code ran during the tests. It doesn't prove that the behaviour is correct, or that the assertions are meaningful.

8. What makes an assertion weak?
An assertion is weak if it is able to pass even if the behaviour is wrong. 

9. What is the appropriate role of GitHub Copilot as a test assistant?
Copilot can help generate test ideas and suggest edge cases, but its suggestions must be reviewed against the requirements and verified by developers before being accepted.

10. What is the Stage 7 engineering rule?
The Stage 7 engineering rule is to focus on what required behaviour each test actually proves. A passing test only provides evidence for the specific behaviour it checks.

## O Stage Completion

Tested Stage 7 main SHA: [complete] 
Full-suite result: python -m pytest, project/, 65 passed, 0 failed
Unresolved defects and effect on baseline: None.
Clean working tree and integration evidence: git status clean on main after pulling.
Stage 8 handover status: Ready for tutor checkpoint.
All tutorial/formative responses and traceability/Copilot decisions complete: F to K and N are completed, just awaiting update results for B-E, and member contributions.
