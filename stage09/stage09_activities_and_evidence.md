# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Session/domain | Needed to find patients and link appointments. |
| Appointment history | Session/domain | Cancelled appointments must stay retrievable (FR-07). |
| Temporary menu choice | Transient | Only used to pick the next action. |
| Practitioner specialty | Session/domain | Part of the registered practitioner record. |
| Debug print output | Transient | Console output only; not stored data. |
| Appointment status | Session/domain | Controls cancellation and conflict checks (FR-05, FR-06). |

What is intentionally lost on exit? All patients, practitioners and appointments. Data is session-only; there is no persistence in Stage 9.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | tuple[datetime, str] | Return (date_time, appointment_id). No validation or side effects. | Appointment read-only properties |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus or None | New list[Appointment] | Filter by practitioner and optional status, sort with the named key. No I/O, no mutation. | Existing Appointment objects and AppointmentStatus enum |
| Service listing | practitioner_id: str, status: AppointmentStatus or None | New ordered list[Appointment] | Reject invalid status (ValueError) and unknown practitioner (LookupError), then call select_appointments. | SmartCareDataStore lookup and list_appointments() |
| Console | User text input | Printed messages | Read and convert input (dates, status), call services, print results, catch ValueError/LookupError and continue. | parse_date_time, AppointmentStatus values, services |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: IDs and names are trimmed, non-blank text (required_text). IDs are read-only. An appointment stores the actual registered Patient and Practitioner objects, a minute-precision naive date_time and an AppointmentStatus enum. Queries read these properties and never change them.
### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | Domain object doing I/O | Console reads input; the domain only changes state and enforces rules. |
| Service prints/reads the menu | Service doing console work | Console handles the menu; services return results or raise errors. |
| Query sorts its source in place | Query mutates its input | Use sorted() to return a new list; the source stays unchanged. |
| Store prints Appointment saved | Store doing output | Store only stores and finds; the console prints messages. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: `.sort()` reorders the source list and returns None. `sorted()` leaves the source order unchanged and returns a new list (result is not appointments). Mutation check: copy the source before the call, then assert source == copy and result is not source.

Score-example prediction and explanation of passing the named key: Passing the named key (not calling it) lets sorted() apply it to each item. Items are ordered by date_time first; equal times are ordered by appointment ID, so the result is always the same.
### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancellation changes status to CANCELLED and keeps the record; deletion would remove history, which FR-07 does not allow. Checks: find the cancelled appointment by ID in the same session; list the practitioner with no filter and see it included; book the same practitioner/time again and see it allowed, because only SCHEDULED appointments cause conflicts.
## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->
The query is a pure function with explicit inputs and no global store, so it is easy to test. The service validates and looks up the practitioner, then calls the query. The console converts text to enum/datetime and handles errors. Results reuse the stored Appointment objects; nothing is copied or changed.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| Practitioner filter | D1 and D2 appointments | select_appointments (query) | Only D1 appointments returned | test_select_orders_and_filters_by_practitioner |
| Status filter / default all | Mixed statuses; status or None | select_appointments (query) | Only matching status; None returns all | test_select_each_status_filter |
| Ordering and tie-break | Unordered times; equal times | select_appointments with appointment_sort_key | Date/time, then ID | test_select_breaks_time_ties_by_id |
| Purity / new list | Source list | select_appointments (query) | Source unchanged; new list returned | test_select_does_not_mutate_source |
| Known practitioner, no matches | D2 with CANCELLED filter | list_practitioner_appointments (service) | Empty list | test_list_known_practitioner_without_matches_is_empty |
| Unknown practitioner | D9 | list_practitioner_appointments (service) | LookupError | test_list_unknown_practitioner_raises_lookup_error |
| Invalid status / ID | "scheduled" text; blank ID | list_practitioner_appointments (service) | ValueError | test_list_invalid_status_raises_value_error, test_list_invalid_id_raises_value_error |
| Retained history | Cancelled A2 | list_practitioner_appointments (service) | A2 still listed | test_list_includes_every_status_by_default |
| Menu workflow | Register, book, cancel, list, exit | run_menu (console) | Data kept until exit | test_menu_register_book_cancel_list_exit |
| Invalid input recovery | Bad option, unknown ID, bad date | run_menu (console) | Error printed, menu continues | test_menu_recovers_from_errors |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: Empty means a known practitioner with no matches and returns []. Unknown means a valid ID that is not registered and raises LookupError. Invalid means a blank ID or a non-enum status and raises ValueError. The console converts status text to AppointmentStatus (blank means all). Results contain the same stored objects (checked with `is`). The console catches ValueError and LookupError, prints the error and continues. Rejected actions leave stored records unchanged.
## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| | | | | |

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
Integrated common Stage 9 SHA: <!-- complete -->
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
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
