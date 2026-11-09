# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: 1.
1. Symptom — “Appointment disappears after cancellation” describes the visible problem.
2. Hypothesis — The removal path is a possible explanation that needs checking.
3. Evidence — The failing test reports a specific result: lookup returns None.
4. Opinion — “Badly designed” is a judgement without supporting evidence.
5. Evidence — The traceback identifies where the error appeared, but not necessarily its cause.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: 
- Expected: FR-07 requires cancelled appointments to remain retrievable.
- Observed: Looking up A1 after cancellation raises LookupError.
- Reproduction: Register P1 and D1, book A1, cancel it, then find A1.
- Initial hypothesis: Lookup may filter out cancelled appointments.
- Evidence to inspect: Store lookup, cancellation methods and list_appointments().
- Finding: Lookup excludes cancelled records even though they remain stored.
- Assistance/timing: This record summarises ChatGPT-assisted analysis and a later reproduction of the faulty version.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: 
Both test expectations are wrong.

A deletion test contradicts FR-07. Change it so that the same cancelled appointment remains retrievable.

A test blocking different practitioners at the same time contradicts AC-04.2. Change it to expect a successful booking.


### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: 

The method is too long, repeats code and does too many jobs. Nested conditions make it harder to follow.

Use smaller methods, the existing status enum and data-store methods. Keep printing in the console.

| Change | Type |
|---|---|
| Rename appt to appointment | Refactoring |
| Extract repeated conflict logic | Refactoring |
| Add rescheduling | Feature |
| Restore cancelled-history lookup | Repair |
| Replace a status string with the enum | Refactoring |

Refactoring must preserve results, exceptions, cancellation rules, booking rules and stored records.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: Changing code too quickly may fix the wrong problem. First repeat the error and check what should happen. Then find the cause, fix it and run the tests again.


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: aa9c654aeccbc70a1e35a1e66da0aa7329bda140
- Baseline test command / working directory / observed result / evidence: - Baseline test command / working directory / observed result / evidence: python -m pytest, run from SmartCare-aa9c654-test/project/. Result: 56 passed in 0.08s. Tested SHA: aa9c654aeccbc70a1e35a1e66da0aa7329bda140. Evidence: terminal output from a later verification of this baseline version.
- Clean preparation SHA if a record-only commit followed Stage 7: Not applicable — no separate record-only commit.
- Branch and preparer / how teammates obtained this branch: Team member Adharv did a session witht eh tutor.
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: 4dc37802259ccb7544915c8a435fffa39fc08126
- Preparation or recovery issues and resolution, if any: 4dc37802259ccb7544915c8a435fffa39fc08126
- Initial prepared full-suite command / result / key failures: 4dc37802259ccb7544915c8a435fffa39fc08126

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: Cancelled appointment A1 cannot be found. Cancelling it again raises LookupError instead of the required ValueError.

- Expected behaviour and requirement: FR-07 requires cancelled appointments to remain retrievable. FR-06 allows cancellation only from SCHEDULED; repeated cancellation must raise ValueError without changing state.

- Minimal synthetic reproduction steps: Register P1 and D1, book A1, cancel it, then find A1 or attempt cancellation again.

- Meaningful failing test path/name and exact relevant failure:
  - tests/test_services.py::test_cancelled_appointment_is_stored — line 129; LookupError: Appointment not found.
  - tests/test_services.py::test_cancelled_twice_keeps_state — line 143; expected ValueError but received LookupError.
  - Both errors are raised at smartcare/services.py:147.

- Human hypothesis and intended checks: See E, F8-01.

- Supported root cause and inspected code/runtime evidence: The inspected find_appointment() code excludes cancelled appointments. The service receives None and raises LookupError before the domain cancellation check can run.

- Smallest justified fix / diff / why other behaviour is preserved: Remove the cancelled-status filter and retrieve by validated ID. Keep ID validation, unknown-ID handling and the existing domain cancellation rules.

- Repair SHA / focused verification result: Pending repair and testing on the restarted branch.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: A second booking for the same practitioner at the same time is incorrectly allowed.

- Expected behaviour and requirement: FR-05 requires same-practitioner/time SCHEDULED bookings to be rejected with ValueError. Different practitioners at that time are allowed.

- Minimal synthetic reproduction steps: Register P1 and D1, book A1 with D1 at 9:00, then attempt A2 with D1 at the same time.

- Meaningful failing test path/name and exact relevant failure: tests/test_starter.py::test_conflict_rule_and_different_practitioner, line 127. Failed: DID NOT RAISE ValueError.

- Human hypothesis and intended checks: See E, F8-02.

- Supported root cause and inspected code/runtime evidence: has_practitioner_conflict() uses != when comparing practitioner IDs. This checks different practitioners instead of the same practitioner, explaining the missing ValueError.

- Smallest justified fix / diff / why other behaviour is preserved: Change the practitioner-ID comparison from != to ==. Keep the existing time, SCHEDULED-status and excluded-appointment checks.

- Repair SHA / focused verification result: Pending repair and testing on the restarted branch.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry

Likely cause and why plausible:
Cancellation may remove the appointment because lookup cannot find it afterwards.

Evidence intended to inspect / competing explanation / discriminating check:
Inspect cancellation and compare the appointment list before and after.
Another possibility is that lookup hides cancelled records. If the record
remains in the list, deletion is unlikely.

Member and saved sequence/time or commit:
SHA 860390bb0c0735894f013e143ccbed8f9ee7d6b0 Memebr KRestianreyes13


### F8-02 human entry

Likely cause and why plausible:
The requested booking time may not match the stored time, causing the
conflict check to miss the existing appointment.

Evidence intended to inspect / competing explanation / discriminating check:
Compare both datetime values. Another possibility is an incorrect
practitioner comparison. If the times match, inspect the practitioner IDs
and comparison operator.

Member and saved sequence/time or commit:
SHA 860390bb0c0735894f013e143ccbed8f9ee7d6b0 Memebr KRestianreyes13

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: krestianreyse13

I am completing SmartCare Assignment 3, Stage 8.

This consultation supports:
- Part C: F8-01 diagnosis and repair.
- Part E: Compare suggestions with my recorded hypothesis.
- Part F: Record Copilot findings, evidence checks and decisions.


Observed behaviour:
After cancelling A1, lookup raises LookupError: Appointment not found.
Repeated cancellation also raises LookupError instead of ValueError.

Expected behaviour:
FR-07 requires cancelled appointments to remain retrievable.
Repeated cancellation must raise ValueError without changing state.

Steps to reproduce:
Register P1 and D1, book A1, cancel A1, then find A1 or cancel it again.

Failing tests:
- test_cancelled_appointment_is_stored, test_services.py:129.
- test_cancelled_twice_keeps_state, test_services.py:143.
Both raise LookupError at services.py:147.

My Part E hypothesis:
Likely cause and why plausible:
Cancellation may remove the appointment because lookup cannot find it afterwards.

Evidence intended to inspect / competing explanation / discriminating check:
Inspect cancellation and compare the appointment list before and after.
Another possibility is that lookup hides cancelled records. If the record
remains in the list, deletion is unlikely.

Relevant faulty code:
    def add_appointment(self, appointment: Appointment) -> None:
        """Store an appointment with the actual registered participant
        objects.

        Raise ValueError for wrong types, duplicate IDs or unregistered
        objects. Do not change stored records when insertion fails.
        """
        if not isinstance(appointment, Appointment):
            raise ValueError('Expected an Appointment object')
        if appointment.appointment_id in self._appointments:
            raise ValueError('Appointment ID already exists')
        if self.find_patient(
            appointment.patient.patient_id,
        ) is not appointment.patient:
            raise ValueError('Patient must be registered in this data store')
        if self.find_practitioner(
            appointment.practitioner.practitioner_id,
        ) is not appointment.practitioner:
            raise ValueError(
                'Practitioner must be registered in this data store',
            )
        self._appointments[appointment.appointment_id] = appointment

    def find_appointment(self, appointment_id: str) -> Appointment | None:
        if not isinstance(appointment_id, str) or not appointment_id.strip():
            raise ValueError("Appointment ID cannot be blank")
        for appointment in self.list_appointments():
            if (appointment.appointment_id == appointment_id.strip()
                    and appointment.status.value != "cancelled"):
                return appointment
        return None

    def list_appointments(self) -> list[Appointment]:
        """Return a new list containing all stored appointment objects."""
        return list(self._appointments.values())

    def has_practitioner_conflict(
        self,
        practitioner_id: str,
        date_time: datetime,
        exclude_appointment_id: str | None = None,
    ) -> bool:
        for appointment in self.list_appointments():
            if (appointment.appointment_id != exclude_appointment_id
                    and appointment.practitioner.practitioner_id != practitioner_id
                    and appointment.date_time == date_time
                    and appointment.status.value == "scheduled"):
                return True
        return False


Task:
Rank three likely causes. For each:
1. Explain why it is plausible.
2. Identify relevant code and available evidence.
3. Suggest a check distinguishing it from the other causes.

Help me evaluate the findings for Part F, but do not invent checks,
results or Accept/Modify/Reject decisions on my behalf.

Do not rewrite the application or invent requirements.
Treat explanations as hypotheses until verified.
Do not claim tests ran.
1. Rank 1 — Lookup hides cancelled appointments.
Evidence check: Inspect find_appointment().
Observed evidence: Its condition excludes "cancelled" status.
Judgement: Correct.
Decision: Accept — this explains why a stored cancelled appointment cannot be found.

2. Rank 2 — Cancellation removes A1 from storage.
Evidence check: Inspect cancel_appointment() and Appointment.cancel().
Observed evidence: They change the status without deleting the record.
Judgement: Wrong as the root cause.
Decision: Reject — the inspected code filters the record from lookup rather than removing it.

3. Rank 3 — Lookup failure prevents the repeated-cancellation status check.
Evidence check: Trace cancel_appointment() through find_appointment().
Observed evidence: Lookup raises LookupError before Appointment.cancel() can reject the repeated cancellation with ValueError.
Judgement: Partly correct.
Decision: Modify — this explains the repeated-cancellation error, but it is a consequence of the lookup bug, not a separate service defect.

Final human conclusion and comparison with initial hypothesis:
The evidence supports lookup filtering as the root cause. The initial removal hypothesis was disproved by inspecting the cancellation methods. Fix the store lookup and keep the existing domain cancellation rules.

### F8-02 Copilot review
Actual prompt / output reference and member: Krestian

I am completing SmartCare Assignment 3, Stage 8.

This consultation supports:
- Part D: F8-02 diagnosis and repair.
- Part E: Compare suggestions with my recorded hypothesis.
- Part F: Record Copilot findings, evidence checks and decisions.



Observed behaviour:
A second booking for the same practitioner at the exact same time
does not raise ValueError.

Expected behaviour:
FR-05 blocks bookings conflicting with a SCHEDULED appointment for
the same practitioner at the exact same time.
AC-04.2 allows different practitioners at that time.

Steps to reproduce:
Register P1, D1 and D2. Book A1 with D1 at 09:00.
Attempt A2 with D1 at 09:00. Separately test D2 at 09:00.

Failing test:
test_starter.py::test_conflict_rule_and_different_practitioner,
line 127: Failed: DID NOT RAISE ValueError.
The test stops before checking the different-practitioner outcome.

My Part E hypothesis:
human entry

Likely cause and why plausible:
Cancellation may remove the appointment because lookup cannot find it afterwards.

Evidence intended to inspect / competing explanation / discriminating check:
Inspect cancellation and compare the appointment list before and after.
Another possibility is that lookup hides cancelled records. If the record
remains in the list, deletion is unlikely.

Relevant faulty code:
class SmartCareDataStore:
    """Own three in-memory collections for one SmartCare session."""

    def __init__(self) -> None:
        """Create an empty store for the current session."""
        self._patients: dict[str, Patient] = {}
        self._practitioners: dict[str, Practitioner] = {}
        self._appointments: dict[str, Appointment] = {}

    def add_patient(self, patient: Patient) -> None:
        """Store a Patient; reject a wrong type or duplicate ID with
        ValueError.
        """
        if not isinstance(patient, Patient):
            raise ValueError('Expected a Patient object')
        if patient.patient_id in self._patients:
            raise ValueError('Patient ID already exists')
        self._patients[patient.patient_id] = patient

    def find_patient(self, patient_id: str) -> Patient | None:
        """Return the stored patient or None; reject blank IDs with
        ValueError.
        """
        return self._patients.get(required_text(patient_id, 'Patient ID'))

    def list_patients(self) -> list[Patient]:
        """Return a new list containing the stored patient objects."""
        return list(self._patients.values())

    def add_practitioner(self, practitioner: Practitioner) -> None:
        """Store a Practitioner; reject wrong types or duplicate IDs with
        ValueError.
        """
        if not isinstance(practitioner, Practitioner):
            raise ValueError('Expected a Practitioner object')
        if practitioner.practitioner_id in self._practitioners:
            raise ValueError('Practitioner ID already exists')
        self._practitioners[practitioner.practitioner_id] = practitioner

    def find_practitioner(self, practitioner_id: str) -> Practitioner | None:
        """Return the stored practitioner or None; reject blank IDs with
        ValueError.
        """
        return self._practitioners.get(
            required_text(practitioner_id, 'Practitioner ID'),
        )

    def list_practitioners(self) -> list[Practitioner]:
        """Return a new list containing the stored practitioner objects."""
        return list(self._practitioners.values())


Task:
Rank three likely causes. For each:
1. Explain why it is plausible.
2. Identify relevant code and available evidence.
3. Suggest a check distinguishing it from the other causes.

Help me evaluate the findings for Part F, but do not invent checks,
results or Accept/Modify/Reject decisions on my behalf.

Do not rewrite the application or invent requirements.
Treat explanations as hypotheses until verified.
Do not claim tests ran.



1. Rank 1 — Practitioner comparison is reversed.
Evidence check: Inspect has_practitioner_conflict().
Observed evidence: It uses != instead of == for practitioner IDs.
Judgement: Correct.
Decision: Accept — this skips the same practitioner and can incorrectly block different practitioners.

2. Rank 2 — Booking does not call or enforce the conflict check.
Evidence check: Inspect book_appointment().
Observed evidence: It calls the checker and raises ValueError when True is returned.
Judgement: Wrong as the root cause.
Decision: Reject — the service already calls and enforces the check.

3. Rank 3 — Time or status values do not match.
Evidence check: Inspect the failing test and appointment construction.
Observed evidence: Both bookings use the same datetime, and A1 defaults to SCHEDULED.
Judgement: Wrong for this reproduction.
Decision: Reject — the time and status meet the conflict conditions.

Final human conclusion and comparison with initial hypothesis:
The reversed practitioner comparison explains the failure. My earlier cancellation hypothesis concerned F8-01 and did not explain this booking problem. The fix is to change != to == and verify both same-practitioner rejection and different-practitioner acceptance.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | 4dc37802259ccb7544915c8a435fffa39fc08126 — confirm using git rev-parse HEAD | py -m pytest; project/ | Full suite: 3 failed, 53 passed in 0.25s. test_cancelled_appointment_is_stored and test_cancelled_twice_keeps_state raised LookupError: Appointment not found. Evidence: saved terminal output. |
| F8-01 after repair | 64d1bf9fdc69dc5307e3f0c5cc7ca50599989f50 | py -m pytest tests/test_services.py::test_cancelled_appointment_is_stored -v  |1 passed in 0.03s. test_cancelled_appointment_is_stored confirms the cancelled appointment remains retrievable. Evidence: tests/test_services.py::test_cancelled_appointment_is_stored PASSED                                                                                                                                                                                                                                          [100%]
| 
| F8-02 before repair | Same faulty SHA as above | py -m pytest; project/ | In the same run, test_conflict_rule_and_different_practitioner failed at test_starter.py:127: DID NOT RAISE ValueError. Evidence: saved terminal output. |
| F8-02 after repair | 3ff948717168705590a8d19ff0f01e36c2c6c2ab | py -m pytest tests/test_starter.py::test_conflict_rule_and_different_practitioner -v | 1 passed in 0.03s. test_conflict_rule_and_different_practitioner confirms a same-practitioner/time booking is now rejected and a different practitioner can still book that time. Evidence: tests/test_starter.py::test_conflict_rule_and_different_practitioner PASSED [100%]  |
| Full suite after both repairs, before refactor | 56ff80c14f4add2117a0822b4de0f6e53865f468 | py -m pytest; project/ | 57 passed in 0.07s. The full suite confirms both repairs pass together with no regressions in test_domain.py, test_services.py or test_starter.py. Evidence: tests\test_domain.py, tests\test_services.py and tests\test_starter.py all passed [100%]|

Explain how the assertions detect each relevant incorrect result and protect previous behaviour:
F8-01: The tests check that cancelled A1 can still be found and that a second cancellation raises ValueError. The faulty lookup returned None, so both failed. They also check that the record and its status stay unchanged.

F8-02: The test expects ValueError for a same-practitioner/time booking. The != bug allowed it, so the test failed. It also checks that a different practitioner can still book that time.

The full suite (57 passed) confirms earlier behaviour still works.

Unrelated failures investigated / resolution:
Not applicable. All 3 failures before the repairs were caused by F8-01 and F8-02.

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
