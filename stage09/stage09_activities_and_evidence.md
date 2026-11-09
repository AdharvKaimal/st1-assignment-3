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

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- response -->
What the tests do and do not establish: <!-- response -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
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
