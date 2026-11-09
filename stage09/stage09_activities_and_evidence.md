# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated 1a5e967dd8af6c4069cf1972000d25f0368a859b, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Session/domain | Needed to find patients and link appointments to the actual registered Patient. |
| Appointment history | Session/domain | Cancelled appointments must stay retrievable and listable (FR-07). |
| Temporary menu choice | Transient | Only selects the next action; not stored. |
| Practitioner specialty | Session/domain | Part of the registered practitioner record shown on lookup. |
| Debug print output | Transient | Console display only; not data. |
| Appointment status | Session/domain | Controls cancellation, conflict checks and status filtering (FR-05, FR-06, QRY-02). |

What is intentionally lost on exit? All patients, practitioners and appointments. Data is session-only; FR-10 persistence is retired, so a new session starts empty.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | tuple[datetime, str] | Return (date_time, appointment_id). No validation, no side effects. | Appointment read-only properties |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus or None | New list[Appointment] | Select practitioner, optional status filter, sort with the named key. No I/O, no store, no mutation. Does not check registration. | Existing Appointment objects; AppointmentStatus enum |
| Service listing | practitioner_id: str, status: AppointmentStatus or None | New ordered list[Appointment] | Validate status (ValueError) and practitioner via the store (ValueError blank, LookupError unknown); pass a fresh list_appointments() and the registered ID to the query. | SmartCareDataStore.find_practitioner, list_appointments |
| Console | Typed text | Printed messages | Prompt, parse date/time and status text, call services, display results, catch ValueError/LookupError and return to the menu. | parse_date_time, format_appointment, services |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: All IDs and text fields are trimmed, non-blank text (required_text); IDs are read-only and case-sensitive. An Appointment holds the actual registered Patient and Practitioner objects (checked with `is` by the store), a naive minute-precision date_time and an AppointmentStatus. No new fields are added; queries only read these properties.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | Domain object does console input | The console asks for confirmation; cancel() only enforces the SCHEDULED rule and changes status. |
| Service prints/reads the menu | Service does console I/O | The console owns the menu; services return objects or raise errors so they can be tested and reused. |
| Query sorts its source in place | Query mutates its argument | Use sorted() to return a new list; the caller's list keeps its order. |
| Store prints Appointment saved | Store does output | The store returns/stores objects; the console decides what to print. Returning the object lets callers check identity and keeps the store testable. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: `.sort()` changes the source order and returns None. `sorted()` keeps the source order and returns a new list (`result is not appointments`). Mutation check: snapshot the source as (object, ID, patient, practitioner, date_time, status) for each item before the call, then assert the snapshot is equal afterwards. An unchanged length is not enough because a reorder keeps the length.

Score-example prediction and explanation of passing the named key: `ordered` is `[('Chen', 5), ('Ali', 8), ('Bea', 8)]`; `scores` is unchanged and `ordered is not scores`. Passing `score_key` (not `score_key(...)`) gives sorted() the function to call on each item. Calling it immediately would pass one tuple, not a function. Equal scores are ordered by name.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancellation changes the retained object's status to CANCELLED; deletion would lose history that FR-07 requires. Checks: find A1 after cancelling and confirm it is the same object with CANCELLED status; list D1 with no filter and see A1; list D1 with SCHEDULED and see A1 omitted, because it is no longer scheduled. That is also why its slot can be booked again.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: The query is pure with explicit inputs, so it is tested without a store. The service validates the practitioner through the existing store contract and passes the registered ID, so " D1 " is not a misleading empty result. Status text is converted to the enum only in the console; services accept AppointmentStatus or None. One store and one set of services are used for the whole menu session. Results reuse stored Appointment objects; nothing is copied or changed.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 | D1 and D2 appointments | select_appointments (query) | Only D1; D2 as control | test_qry01_only_requested_practitioner |
| QRY-02 | Scheduled, cancelled, completed for D1 | select_appointments (query) | None = all; each enum returns only that status; no match = [] | test_qry02_default_includes_every_status, test_qry02_each_explicit_status, test_qry02_no_matching_status_is_empty |
| QRY-03 | Unsorted source; equal 09:00 times | select_appointments with appointment_sort_key | Date/time then ID; source unchanged | test_qry03_orders_by_time_then_id_and_keeps_source |
| QRY-04 | Known/unknown/blank ID; enum or text status | list_practitioner_appointments (service) | [] / LookupError / ValueError / ValueError; omitted status keeps history | test_qry04_* in test_workflows.py |
| FP-01 | Same inputs twice | select_appointments (query) | Equal results; no output; source unchanged | test_fp01_repeated_calls_give_same_result, test_fp01_no_output |
| FP-02 | Empty, already-sorted, unsorted lists | select_appointments (query) | Distinct new list; same unchanged objects | test_fp02_* |
| FP-03 | One appointment; source list | appointment_sort_key and select_appointments | Key = (date_time, ID); sorting calls the key | test_fp03_* |
| FR-01–09 workflow | Register, book, conflict, cancel, find, list, freed slot | Services | Rejections keep state; history kept; slot reusable | test_service_workflow_preserves_state_and_history |
| UI-01 | Full demonstration input | run_menu (console) | All steps succeed; conflict rejected; history listed | test_ui01_full_menu_workflow, test_real_console_process_runs_ui01 |
| UI-02 | Invalid inputs | run_menu (console) | Error shown, menu continues, state unchanged | test_ui02_invalid_input_recovery |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: Empty: a known practitioner with no matches returns a new []. Unknown: a valid but unregistered ID raises LookupError. Invalid: a blank/non-string ID or a non-enum status (such as 'scheduled' text) raises ValueError, not an empty result. The console converts typed status to the enum (blank = all) and rejects other text. Results contain the stored objects themselves (checked with `is`). The console catches only ValueError and LookupError, prints the message and returns to the menu. Rejected operations leave the stored records unchanged (before/after checks in the workflow and UI-02 tests).
## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---| 
| QRY-01 test_qry01_only_requested_practitioner | queries.py select_appointments | D1 → A1, A3, A5, A4; D2 → A2 only | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| QRY-01 test_qry01_unmatched_practitioner_returns_empty | queries.py select_appointments | D9 → [] | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| QRY-02 test_qry02_default_includes_every_status | queries.py select_appointments | None includes all three statuses | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| QRY-02 test_qry02_each_explicit_status | queries.py select_appointments | SCHEDULED → A3, A4; CANCELLED → A1; COMPLETED → A5 | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| QRY-02 test_qry02_no_matching_status_is_empty | queries.py select_appointments | D2 + CANCELLED → [] | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| QRY-03 test_qry03_orders_by_time_then_id_and_keeps_source | queries.py select_appointments | Equal 09:00 ordered A1, A3, A5 then A4 at 10:00; source snapshot unchanged | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| FP-01 test_fp01_repeated_calls_give_same_result | queries.py select_appointments | Repeat call equal, new list, source unchanged | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| FP-01 test_fp01_no_output | queries.py | Nothing printed | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| FP-02 test_fp02_empty_source_gives_new_list | queries.py select_appointments | [] and `result is not source` | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| FP-02 test_fp02_already_sorted_source_gives_new_list | queries.py select_appointments | Equal but distinct list | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| FP-02 test_fp02_unsorted_source_reuses_unchanged_objects | queries.py select_appointments | Same objects (`is`), fields unchanged | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| FP-03 test_fp03_named_key_value | queries.py appointment_sort_key | Key = (10:00, 'A4') | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| FP-03 test_fp03_key_does_not_change_appointment | queries.py appointment_sort_key | Snapshot unchanged after key calls | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| FP-03 test_fp03_sorting_uses_named_key | queries.py select_appointments | Recording key called for every D1 appointment | PASSED | tests/test_queries.py, SHA [1a5e967dd8af6c4069cf1972000d25f0368a859b] |
| QRY-04 test_qry04_known_practitioner_without_appointments | services.py list_practitioner_appointments | Known D1, no bookings → [] | PASSED | tests/test_workflows.py, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |
| QRY-04 test_qry04_known_practitioner_without_matching_status | services.py list_practitioner_appointments | CANCELLED filter, none → [] | PASSED | tests/test_workflows.py, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |
| QRY-04 test_qry04_unknown_practitioner_raises_lookup_error | services.py list_practitioner_appointments | D9 → LookupError | PASSED | tests/test_workflows.py, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |
| QRY-04 test_qry04_blank_or_invalid_id_raises_value_error | services.py list_practitioner_appointments | '', '   ', None, 1 → ValueError | PASSED | tests/test_workflows.py, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |
| QRY-04 test_qry04_text_status_raises_value_error | services.py list_practitioner_appointments | 'scheduled' → ValueError; store unchanged | PASSED | tests/test_workflows.py, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |
| QRY-04 test_qry04_omitted_status_keeps_history | services.py list_practitioner_appointments | Cancelled A1 listed, same object | PASSED | tests/test_workflows.py, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |
| QRY-04 test_qry04_uses_registered_id_for_trimmed_input | services.py list_practitioner_appointments | ' D1 ' finds A1 | PASSED | tests/test_workflows.py, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |
| QRY-04 test_qry04_returns_fresh_list | services.py list_practitioner_appointments | Repeated calls equal, distinct lists | PASSED | tests/test_workflows.py, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: select_appointments reads only its three arguments, builds a new list with a comprehension and returns sorted(..., key=appointment_sort_key). It has no print/input, no global or module-level state, no store or service call, and never assigns to the source list or Appointment objects. appointment_sort_key only reads two read-only properties.

What the tests do and do not establish: They show correct results, new lists and unchanged sources for the tested inputs, and that the named key is used. They support purity but do not prove it for every possible input; code inspection covers hidden state and I/O. They do not test performance, overlapping durations or persistence (out of scope).

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | stage09/evidence/ui01_input.txt; from project/: Get-Content ../stage09/evidence/ui01_input.txt \| py main.py --interactive | P1, D1, D2 registered and found; A1 booked; A-CONFLICT rejected; A2 with D2 allowed; A1 cancelled and found as Cancelled; D1 all = A1, Scheduled = none; A3 booked in freed slot; final list A1, A3; Goodbye | [Matched expected / describe any difference]. Final D1 list showed A1 (Cancelled) and A3 (Scheduled), "2 appointments found." | stage09/evidence/ui01_output.txt; tests/test_workflows.py::test_ui01_full_menu_workflow, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |
| UI-02 invalid-input recovery | stage09/evidence/ui02_input.txt; same command with ui02_input.txt | Each error shown (unknown choice, blank/unknown ID, duplicate, unknown participant, malformed and impossible date, unknown appointment, repeated cancel, invalid status); menu continues; A9 not reserved and later books; P1 still Alex Example | [Matched expected / describe any difference]. After the errors, A9 booked successfully and P1 was found as Alex Example. | stage09/evidence/ui02_output.txt; tests/test_workflows.py::test_ui02_invalid_input_recovery, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |
| Automated service workflow | tests/test_workflows.py::test_service_workflow_preserves_state_and_history; also test_real_console_process_runs_ui01 | Duplicate, unknown participant, duplicate ID and conflict rejected with store unchanged; D2 allowed; A1 cancelled but found and listed; SCHEDULED filter empty; A3 books freed slot | PASSED | tests/test_workflows.py, SHA [db5afaf0331a0699c3fd23afce10ca4348db53fb] |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: Parts A and B, commit SHA 5baa41c6e8e20fefb826fc60d4059a431db624b4
Actual prompt/context supplied: Handout section 8 prompt with queries.py, services.py, console.py, main.py and test summaries (QRY-01–04, FP-01–03, UI-01–02). See stage09/evidence/copilot_review.md.
Actual response: stage09/evidence/copilot_review.md

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| Query, service listing and run_menu still raise NotImplementedError | queries.py, services.py list_practitioner_appointments, console.py run_menu on branch Stage9/testing/and/Doc | Critical (AI) | Reject. Copilot reviewed the starter stubs, not the current branch. All three are implemented. | No change | Inspected the three files; py -m pytest -v: test_queries.py and test_workflows.py PASSED |
| Retained history and listing not proven at service level | test_qry04_omitted_status_keeps_history, test_service_workflow_preserves_state_and_history | Critical (AI) | Reject. Based on the same stale code. Tests show cancelled A1 is found and listed as the same object. | No change | Both tests PASSED |
| Interactive console incomplete; main.py catches NotImplementedError | main.py, console.py | Critical (AI) | Reject. main.py now calls run_menu() directly and the menu is complete. | No change | test_ui01_full_menu_workflow and test_real_console_process_runs_ui01 PASSED; UI-01 run saved |
| Check purity: new list, source order and identities unchanged | test_qry03_*, test_fp01_*, test_fp02_* | Important | Accept the check, not a change. It matches our design and is already tested with before/after snapshots. | No change | FP-01, FP-02, QRY-03 tests PASSED |
| Enum filtering and object identity must be verified | test_qry02_*, test_fp02_unsorted_source_reuses_unchanged_objects, test_qry04_text_status_raises_value_error | Important | Accept the check. Already covered: None = all, each enum, same objects (`is`), text status rejected. | No change | Tests PASSED |
| Required QRY/FP/UI verifications missing | tests/test_queries.py, tests/test_workflows.py | Important (AI) | Reject. The tests exist; Copilot did not see them. | No change | py -m pytest -v: all tests PASSED |
| Recovery and unchanged state only documented | test_ui02_invalid_input_recovery, test_service_workflow_preserves_state_and_history | Optional | Reject. Demonstrated by UI-02 (error, then successful action) and before/after store checks. | No change | Tests PASSED; UI-02 run saved |

Copilot's main conclusion was wrong because it reviewed outdated code. Each claim was checked against the actual branch files and test results before any decision; no code was changed. Its structural comments (domain, store and service separation; enum identity with `is`) agreed with our design.

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: Appointment still owns the cancellation rule; the store owns collections and identity checks; services coordinate validation and call the query; the query only selects and sorts; the console only prompts, converts text, calls services and prints. No layer prints or reads input except the console.
## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? Deciding where each check belongs. The service checks the practitioner is registered, the console turns status text into the enum, and the query only filters and sorts. One store is used for the whole session so data stays until exit.

2. Which Copilot suggestion did you reject as over-engineering, and why? Copilot did not suggest over-engineering. We rejected its claim that the code was unimplemented, because it had reviewed the old starter files. The current code and passing tests showed this was wrong.

3. How did you prove cancelled appointments remain retrievable and listable in the same session? Tests cancel A1, then find it by ID and see it in the full list but not in the SCHEDULED list. The UI-01 run shows the same, and A3 can then book the freed slot.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? It uses only its arguments, returns a new list and changes nothing. Printing, reading input, using a global store or sorting the source in place would break it.
2. Which explicit inputs are needed, and why avoid a global store? The appointment list, practitioner ID and optional status. A global store hides inputs, makes results depend on hidden state and makes testing harder.
3. How can a new list reuse Appointment objects safely? The list is new, but it holds the same objects. That is safe because the query only reads them and never changes their fields.
4. Why use a named key, and what breaks equal-time ties? A named key is reusable and can be tested directly. Equal date/times are ordered by appointment ID.
5. How do default and explicit status filters differ? None (default) returns every status, including CANCELLED and COMPLETED. An explicit enum returns only appointments with that status.
6. How do empty, unknown practitioner and invalid filter cases differ? Empty: a known practitioner with no matches returns []. Unknown: a valid but unregistered ID raises LookupError. Invalid: a blank ID or non-enum status raises ValueError.
7. Which console errors recover, and how is unchanged state checked? ValueError and LookupError from bad choices, IDs, dates, statuses, duplicates, conflicts and repeated cancellation. State is checked by listing or finding records afterwards and by a later successful action, such as booking the rejected ID.
8. What is data integrity for registered participants, conflicts and history? Appointments link only the actual registered objects, a practitioner never has two SCHEDULED appointments at the same time, and cancelled appointments are kept, not deleted.
9. What is Copilot's review role, and who verifies findings? Copilot suggests possible issues. The team checks each finding against the code, requirements and tests, and decides Accept/Modify/Reject.
10. How do pure functions and OOP responsibilities work together? Objects and services own rules and state changes; pure functions only select and sort what they are given. The console calls services and never enforces domain rules itself.

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: (https://github.com/copilot/c/8b43ceb7-2eef-449a-9d2a-2f37d314b557)
Integrated common Stage 9 : <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common  protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
