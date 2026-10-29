# Stage 7 Testing and Verification Record

Group/tutorial: Tuesday Group 4 (13:30-15:30)  
Members/cohorts: (GitHub) AdharvKaimal, kristianreyes13, jesshall902
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
[response]

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
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [complete]
Acceptance criterion: [quote]
Behaviour to test: [complete]
Human-first test idea/categories: [complete]
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[response]

2. What question does validation answer?
[response]

3. What is a unit test?
[response]

4. What is a pytest fixture?
[response]

5. What is parametrisation in pytest?
[response]

6. What is regression testing?
[response]

7. What does code coverage tell us, and what does it not prove?
[response]

8. What makes an assertion weak?
[response]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
