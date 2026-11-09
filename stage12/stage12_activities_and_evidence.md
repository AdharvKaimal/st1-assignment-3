# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Tuesday Group 4 (13:30–15:30)
Members and UG/PG applicability:
- AdharvKaimal (UG)
- krestianreyes13 (UG)
- jesshall902 (UG)


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare v1.0 Release Candidate. Requirements Baseline Revision 2.
Common starting SHA / branch / applicable members: *STAGE9_SHA* on main. AdharvKaimal, krestianreyes13 and jesshall902 (all UG).
PG starting SHA / branch / applicable members or not applicable: Not applicable.
Working-state review and approved integration: Stage 8 repairs and refactoring completed and verified before Stage 9 development.
Protected common candidate and PG differences: UG scope includes FR-01 to FR-09 and Stage 9 query and console requirements. PG extensions do not apply.
Feature freeze / owner / verifier: We stopped adding features once Stage 9 was merged. Owner: jesshall902. Verifier: krestianreyes13.


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: Release with conditions. All the tests pass, but the setup steps are incomplete, one dependency hasn't been checked and a known limitation isn't written down. Before sign-off we would finish the README, check where the dependency comes, write the limitation into the README, and re-run all the tests on the exact version we release.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Stage 7 retained-history tests and Stage 8 defect repair | test_cancelled_appointment_is_stored; Stage 8 regression evidence | jesshall902 | Yes | Reconfirmed in the final test run |
| Architecture responsibilities are appropriate | Domain, store, services, pure queries and console each have their own job | domain.py, data_store.py, services.py, queries.py | jesshall902 | Yes | Reconfirmed in the final review |
| Rescheduling is safe — PG only | N/A | N/A | N/A | N/A | N/A |
| AI use is responsible — common recheck / PG assurance | Stage 6, 7, 8 and 9 Copilot reviews | Stage 6 H-I, Stage 7 H-I, Stage 8 F, Stage 9 E | jesshall902 | Yes | Final AI review in section E |
| System is maintainable | Separate responsibilities and accumulated regression tests | project/, tests/ | jesshall902 | Yes | Cleanup in section H |
| FR-01–03 register/find and validation | Stage 6 and 7 domain/service tests | test_domain.py, test_services.py | krestianreyes13 | Yes | Reconfirmed in the final test run |
| FR-04–05 booking/conflict rules | Conflict tests and the Stage 8 practitioner-conflict repair | test_conflict_rejected_and_store_unchanged; Stage 8 evidence | krestianreyes13 | Yes | Reconfirmed in the final test run |
| FR-06–08 cancellation/history/find | Cancellation and retained history tests | test_cancelled_appointment_is_stored, test_cancelled_twice_keeps_state | krestianreyes13 | Yes | Reconfirmed in the final test run |
| FR-09 and QRY/FP listing/filter/order/purity | Stage 9 query and service tests: practitioner filter, default all statuses, each status, empty vs unknown vs invalid, order by date/time then ID, new lists and unchanged source | tests/test_queries.py and tests/test_workflows.py (Stage 9 record, Section C)| jesshall902 | Yes | Reconfirmed in the final test run |
| UI full console sequence and error recovery | test_ui01_full_menu_workflow, test_real_console_process_runs_ui01, test_ui02_invalid_input_recovery | Stage 9 record, section D | krestianreyes13 | Yes | Checked again in the final demo |
| Session-only scope / FR-10 retired | SmartCareDataStore keeps three in-memory dictionaries that only last for the current run. There is no database or file storage in project/. | project/smartcare/data_store.py at a14ef34 | jesshall902 | Yes | Said in the README |
| PG RES and assurance integration | N/A | N/A | N/A | N/A | N/A |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | Python 3.14.3 on Windows, pytest 8.3.5 | project/ ; python -m pytest -q | a14ef34 | 95 passed, 0 failed | https://github.com/AdharvKaimal/st1-assignment-3/commit/a14ef34 |
| Complete PG if applicable | N/A | N/A | N/A | N/A | N/A |
| Affected focused checks after correction | Python 3.14.3 on Windows, pytest 8.3.5 | project/ ; python -m pytest tests/test_services.py -q | a14ef34 | All passed | https://github.com/AdharvKaimal/st1-assignment-3/commit/a14ef34 |
| Full integrated recheck | Python 3.14.3 on Windows, pytest 8.3.5 | project/ ; python -m pytest -q on main after the last merge | a14ef34 | 95 passed, 0 failed | https://github.com/AdharvKaimal/st1-assignment-3/commit/a14ef34 |


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | Small clinic booking appointments | Explain the need for stakeholders: patients, practitioners, reception staff | Explained before the demo: the clinic needs to book and cancel appointments without double-booking practitioners. | Spoken in the demo |
| Register and find Patient and two Practitioners | P1 Alex Example, D1 Taylor Example (General), D2 Morgan Example (General), find each, try an unknown ID | FR-01 to FR-03, ValueError vs LookupError, back to a usable menu | The patient and both practitioners were registered and found as the same stored objects. An unknown ID gave a not-found message and the menu still worked. | test_register_patient_stores_valid_data, test_find_patient_unknown_id, test_find_practitioner_returns_stored_object, test_ui01_full_menu_workflow |
| Valid booking | A1: P1 with D1 at 2026-10-01 09:00 | FR-04 / AC-03.1: stored as SCHEDULED | A1 was stored as SCHEDULED and could be found again. | test_registration_and_booking, test_ui01_full_menu_workflow |
| Same practitioner exact-time conflict rejected | A2: D1 at 09:00 again | FR-05 / AC-04.1: ValueError, no partial appointment | A2 was rejected and only A1 was left. | test_conflict_rejected_and_store_unchanged |
| Different practitioner same time allowed | A3: D2 at 09:00 | FR-05 / AC-04.2: SCHEDULED | A3 was accepted as SCHEDULED. | test_conflict_rule_and_different_practitioner |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel A1, then find A1 | FR-06 / FR-07: same object, status CANCELLED | A1 changed to CANCELLED and could still be found as the same object. | test_cancel_same_object_return_cancelled, test_cancelled_appointment_is_stored |
| Invalid/repeated cancellation rejected | Cancel A1 again, cancel an unknown ID | AC-05.3: ValueError, unknown ID LookupError, state unchanged | Cancelling A1 again was rejected and it stayed CANCELLED. An unknown ID gave a not-found message. | test_cancelled_twice_keeps_state, test_cancel_unknown_id |
| Default all-status listing | List D1's appointments with no filter | FR-09 / QRY-02: all statuses included | The list included the SCHEDULED, CANCELLED and COMPLETED appointments for D1. | test_qry02_default_includes_every_status |
| Explicit filtering / empty vs unknown / deterministic order | Filter by SCHEDULED, a known practitioner with no matches, an unknown practitioner | QRY-02 to QRY-04: only that status; empty list vs LookupError; ascending date/time then ID | The filter returned only that status. A known practitioner with no matches gave an empty list, an unknown one raised LookupError, and appointments at the same time were ordered by ID. Equal-time ties are checked in the tests because the menu can't easily create them. | test_qry02_each_explicit_status, test_qry02_no_matching_status_is_empty, test_qry03_orders_by_time_then_id_and_keeps_source, test_qry04_* |
| Invalid date/status/menu/lookup recovery and continued operation | A bad date, a bad status, an unknown menu choice | UI-02: message shown, menu still usable, state unchanged | Each bad input showed an error and returned to the menu, and the next valid action worked. | test_ui02_invalid_input_recovery |
| Session-only limitation and normal exit | Exit | Data is lost when the process ends | The program exited normally. Data is only kept while it runs, and we didn't demonstrate restarting with saved data. | test_real_console_process_runs_ui01 |
| One meaningful requirement-linked pytest test explained | python -m pytest tests/test_services.py::test_cancelled_appointment_is_stored -v | FR-07 / AC-05.2 | Cancels a booked appointment, then checks find_appointment('A1') is the same object and list_appointments() still holds it. It shows the record is kept and can be found. It doesn't show what the console prints. | Stage 7 record, Section F |
| Architecture and one actual AI decision / known limitation | Domain / store / service / query / console responsibilities | Appointment owns the cancel rule, the service coordinates through the shared store, queries are pure | AI decision: Copilot said to remove the trimming tests, but we rejected that because the Stage 6 handout says IDs are trimmed and data_store already does it. Limitation: data is only kept for the current run. | Stage 6 record, section H |
| PG reschedule identity/participants/time and no-op | N/A | N/A | N/A | N/A |
| PG conflict/invalid status/failure non-mutation | N/A | N/A | N/A | N/A |
| PG old slot / current lookup/list ordering / assurance risks | N/A | N/A | N/A | N/A |
Stable demo owner / fresh process / command: jesshall902; a new terminal; cd project, then python main.py --interactive
PG demonstrations through service/tests or not applicable: Not applicable.


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | domain.py, data_store.py, services.py, queries.py, the console menu | No finding. Domain, store and services have separate jobs. select_appointments and appointment_sort_key are pure functions with explicit inputs, and the console owns all input and output. | No change |
| PascalCase and snake_case naming | Repository source files | No finding. Naming follows Python conventions. | No change |
| Useful type hints and meaningful docstrings | domain.py, data_store.py, services.py, queries.py | Any old "Stage 6 TODO" docstrings that were found were rewritten to describe what the methods do now. | Rewrote them if found, then re-ran all the tests (see C) |
| Four-space indentation and imports/layout | Repository source files | No finding. Layout follows course conventions. | No change |
| Focused methods / duplication / dead or commented code | Current project source | Any leftover commented-out code that was found was deleted. | Deleted it if found, then re-ran all the tests (see C) |
| Globals / leakage / unnecessary inheritance or frameworks | project/smartcare/ | No finding. No global data; the only inheritance is the Enum. | No change |
| No SQLite/persistence/repository ABCs/speculative features | project/ | No finding. No database, files or abstract classes. | No change |
| Synthetic data / secrets / dependencies / provenance | requirements-dev.txt; git ls-files | No finding on data or secrets. Any editor file that was tracked (e.g. .idea/) was untracked and added to .gitignore. Dependencies come from requirements-dev.txt (from the starter). | Untracked it if found; no other change |
| Significant common Copilot contributions and human verification | Stage 6 H-I, Stage 7 H-I, Stage 8 F, Stage 9 E | Each Copilot suggestion was checked against the code and the requirements (table below). | Final diff reviewed |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | N/A | N/A | N/A |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| The trimming tests add a requirement that isn't specified, so remove them (Stage 6, PR #7) | FR-02 lookup, test_services.py | The Stage 6 handout says IDs are trimmed, and data_store already trims them | Reject: trimming is a real rule | Tests kept |
| "No blocking issues" on PR #6 (Stage 6) | FR-02, FR-06, FR-07, services.py | Looked at the diff: an unrelated .idea file, no tests in the PR, old docstrings | Modify: the requirement findings were right but the verdict was too strong | Tests added in PR #7; cleanup in section H |
| Booking might not call the conflict check (Stage 8, F8-02) | FR-05, book_appointment | Read book_appointment: it does call and enforce the check | Reject: wrong cause | Real cause was != instead of == in has_practitioner_conflict |


## F README and reproducibility check
    
| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | project/README.md | jesshall902 | Clear |
| Out-of-scope capabilities and known limitations | project/README.md | jesshall902 | Clear |
| Confirmed teaching Python version and dependency installation | project/README.md | jesshall902 | Worked |
| Working directory / demo / interactive / test commands | project/README.md | jesshall902 | Worked |
| Repository structure and architecture responsibilities | project/README.md | jesshall902 | Clear |
| Responsible AI summary / synthetic-data rule | project/README.md | jesshall902 | Clear |
| Release label/version and SHA links | root README.md | jesshall902 | Matches a14ef34 |

## G Known limitations debt and release notes

Delivered features:
Register and find patients and practitioners. Book appointments and stop a second booking for the same practitioner at the same time. Cancel appointments, which stay in the system as CANCELLED. Find an appointment. List a practitioner's appointments with an optional status filter, in order by date and time then ID. A console menu that recovers from bad input. All data is made up and only lasts while the program runs.

Important fixes:
In Stage 8 we fixed two bugs. Cancelled appointments couldn't be found because lookup skipped them, which also made a second cancellation give the wrong error. And the conflict check compared practitioners with != instead of ==, so double bookings were allowed.

Architecture/quality improvements:
The domain objects, data store, services, pure queries and console each have their own job. In Stage 8 we replaced a hard-coded status string with the AppointmentStatus enum. In Stage 9 the listing and sorting became pure functions that return new lists and don't change their inputs. In Stage 12 we cleaned up leftover comments and old docstrings if there were any.

Known limitations:
Data is lost when the program closes. Times are local and only accurate to the minute. There is no login, patient portal, SMS or email, billing, or clinical advice. It is only meant for one user at a time.

AI-assisted development note:
We used GitHub Copilot to review code, suggest test ideas and rank possible causes of bugs. We treated its answers as suggestions and checked them against the code and requirements, and rejected some. Some of us also used ChatGPT and another AI assistant to help draft analysis, tests and records, and we edited and ran everything ourselves.

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Patient and Practitioner names can be changed after creation without being checked again | A blank name could be set later | Low | Make them checked properties | Accepted: nothing in the current requirements changes names |
| Domain tests for rejected cancellations don't check the status afterwards | A rejection could change the status without those tests noticing | Medium | Add the checks | Accepted: the service tests do check it |
| Failed lookups aren't shown to leave the stores unchanged | Low risk | Low | Add a test | Accepted |
| Data isn't saved | Everything is lost on exit | Scope | Add storage in a later version | Accepted: out of scope (FR-10 retired) |
Session-only synthetic data and minute-precision local time: All data is made up and only lives while the program runs. Times are local and only accurate to the minute.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: None exist.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: It only handles one user in one program. It has no timezone handling or monitoring, and we haven't tested usability or accessibility.
Difference between accepted scope limit and unresolved required behaviour: These are limits of scope, not bugs. Nothing here breaks a current requirement.
PG assurance residual risks / owner / status or not applicable: Not applicable.


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Maintainability: old docstrings, leftover commented code and tracked editor files | Checked with git grep and git ls-files. The Stage 6 review had flagged "Stage 6 TODO" docstrings, commented lines in find_patient and find_practitioner, and an .idea file. | Low, no change to behaviour | jesshall902: remove whatever the checks still found | The Stage 12 cleanup commit (see I) | All tests re-run and passed (see C) | None |
Justified no-change conclusion if no defect found: We checked the requirements and the demo against the final code and found no defect that breaks a current requirement.
Release blockers still open / status: None.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA:
Stage 6: PRs #6 and #7. Stage 7: PR #14. Stage 8 and Stage 9 review and integration evidence are recorded in section I of those records. Stage 12 cleanup and release-review changes are recorded in the final Stage 12 PR.

Independent reviewer / feedback / response:
Each PR was reviewed by a team member other than its author. Feedback, responses and approvals are recorded in the corresponding PRs and stage records.

Integration commit / full recheck:
Merged to main at a14ef34. Running python -m pytest -q from project/ produced 95 passing tests with no failures.

Tracked and untracked file inspection / cleanliness:
git ls-files and git status --short were checked before creating the release ZIP. Tracked and untracked files were reviewed before submission.

Secrets/staff material/caches/tool-metadata exclusion check:
No passwords, credentials, real patient information, staff materials, caches, environments or Stage 8 utility files were present in the tracked release files.

Candidate recovery plan / known-good SHA:
The candidate can be recovered using the reviewed release commit a14ef34. Any future correction would use a reviewed revert or corrective commit rather than deleting history.

Named substantive contributions:
Individual implementation, testing, review, documentation and integration contributions are recorded in the Stage 6–9 records and summarised in section N.


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: READY WITH DOCUMENTED LIMITATIONS

Approver / date / rationale and evidence: Approved by jesshall902 on 9/11/26. The regression suite passed on a14ef34, demonstration requirements were completed, README instructions were verified and known limitations were documented.

What risks remain / conditions / owners: Data is session-only and is not saved when the program exits. SmartCare does not implement authentication, notifications, billing or persistent storage. These limitations are documented in section G. Responsibility for future improvements remains with the development team.

Can the team explain the system: Yes. Team members prepared the explanation topics in section N and can explain requirements, architecture, testing, debugging and release decisions.

Can a change be recovered: Yes. The release candidate can be recovered from a14ef34 using Git history and reviewed commits.

Common decision / PG decision where different: Common UG decision only. PG-specific requirements are not applicable.


## K Final tested release SHA

Exact common tested SHA: a14ef34
Exact PG tested SHA or not applicable: Not applicable.
Final submitted SHA / repository URL: https://github.com/AdharvKaimal/st1-assignment-3
Evidence-only later commit and difference explanation: Any later commit contains documentation or evidence-only updates. No executable source changes were made after the final verified test run.
Executable changes after testing and re-verification: None.
Source ZIP name / SHA correspondence / extracted comparison: Not yet prepared. The source ZIP will be generated from SUBMITTED_SHA during final submission preparation and verified against the repository before upload.


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: As published by the teaching team.
Deadline/timezone: As published by the teaching team.
Repository access arrangement: Public GitHub repository accessible to teaching staff:
https://github.com/AdharvKaimal/st1-assignment-3
Mixed-candidate upload arrangement: Not applicable. 
Oral/video recording/accessibility arrangements: As published by the teaching team.
Remaining administration or release dependency: Replace placeholders with the final verified values before submission. Complete the final checklist after release packaging and verification.


## M Formative questions

1. What is a release candidate?
A version of the software that the team thinks is ready to be released.

2. What is feature freeze and why is it used?
Stopping new features and only fixing real problems, so the code doesn't change (or break) after it's been tested.

3. What is regression testing in a release context?
Running all the earlier tests again on the final version to check old behaviour still works.

4. What is a known limitation?
Something the software doesn't do, which we know about and note down.

5. What is technical debt?
Shortcuts or weak spots in the code or tests that make later changes harder.

6. What are release notes?
A short summary of what the release delivers, what was fixed, and its limitations.

7. What is software maintenance?
The work regularly completed after release to keep it working, such as fixing bugs and updating it.

8. What is the purpose of the individual demonstration/viva?
To show each person understands the whole system and what they contributed.

9. What should the final responsible-AI check establish before release?
That a person checked every AI suggestion and that it matches the requirements. Ensure that all AI use has been recorded honestly.

10. What is the main course conclusion about AI and the role of the software engineer?
AI can write code, but engineers decide what to build, check it and are responsible for it.


## N Reflection viva and handover

Strongest evidence SmartCare is ready:
The strongest evidence is the requirement-linked regression suite. Registration, booking, practitioner conflicts, cancellation, retained history, queries and console workflows are all verified through automated tests and integrated demonstrations.

Weakest area:
The weakest area is session-only storage. Data is intentionally lost when the application exits, which limits realism compared with a production system

How AI use changed from Stage 1 to Stage 12:
At first we used AI mainly for explanations and drafting ideas. By the later stages we treated Copilot and other AI tools as sources of suggestions that had to be checked against requirements, code and test evidence before being accepted.

Start doing — engineering and AI use:
Record evidence and design decisions as we work, and verify AI suggestions against requirements before implementation.

Stop doing — engineering and AI use:
Leaving generic placeholder text in records and accepting suggestions before checking supporting evidence.

Continue doing — engineering and AI use:
Using peer review, regression testing and requirement traceability before merging changes, and documenting AI decisions honestly.

What worked / caused rework / future delivery improvement:
Requirement traceability and cumulative testing worked well. Most rework came from documentation that did not match the code or from delayed integration. In future, we would maintain a single verified list of SHAs, test counts and evidence links throughout the project.

One paragraph — If AI can write code why do we still need software engineers:
AI can generate code quickly, but it cannot determine requirements, judge correctness or take responsibility for release decisions. Software engineers decide what the system should do, evaluate evidence, verify behaviour through testing, identify defects and make accountable decisions about quality and safety. During SmartCare, AI suggestions were useful starting points, but human review, testing and judgement were required before any change was accepted or released.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | A small clinic needs to book and cancel appointments without double-booking practitioners. Stakeholders are patients, practitioners and reception staff. |
| Two requirements and acceptance criteria | FR-05: the same practitioner at the exact same time with a SCHEDULED appointment is a conflict (AC-04.1), but a different practitioner is allowed (AC-04.2). FR-06 and FR-07: cancelling a SCHEDULED appointment makes it CANCELLED (AC-05.1), cancelling again is rejected (AC-05.3), and the cancelled appointment stays findable (AC-05.2). |
| Domain model and architecture | Patient, Practitioner and Appointment hold their data and rules. AppointmentStatus is an enum. SmartCareDataStore holds the data for the session. Services coordinate the actions. The console handles input and output. select_appointments and appointment_sort_key are plain functions. |
| Design trade-off | The cancel rule is inside Appointment, so the rule stays with the object that owns the status. The service then has to rely on it. |
| Meaningful test and its limits / 100 percent coverage | test_cancelled_appointment_is_stored shows the cancelled appointment is the same stored object. It doesn't show what the console prints. 100 percent coverage only means every line ran, not that the checks were good. |
| Diagnosed defect and verification | Stage 8 F8-01 and F8-02, with failing and passing runs in section G of that record. |
| Shared store and session-state/query responsibilities | All services use one SmartCareDataStore, so conflict checks and lookups see the same records. The queries take their inputs (a list, a practitioner ID and a status) and return a new list without changing anything. |
| What would break if session-state lookup/query responsibilities changed? | F8-01 showed it. When the store lookup hid cancelled appointments, FR-07 broke and a second cancellation gave LookupError instead of ValueError. If the query used a global store, it couldn't be tested without one. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Appointment.cancel() owns the rule that only SCHEDULED can be cancelled. A conflict needs all the appointments, so the service asks the shared store. |
| FR-07 retained history test | test_cancelled_appointment_is_stored (also in D). |
| Actual AI change rejected/modified or honestly accepted with verification | We rejected Copilot's advice to remove the trimming tests, because the handout's lookup contract says IDs are trimmed. |
| Unresolved limitation / future production work | Data isn't saved. A real version would need storage, login and roles, and privacy and security checks. |
| Personal implementation contribution | I didn't write the Stage 6 service methods. My work was the tests for them and the extended service tests in Stage 7. |
| Personal test/review/design/integration contribution | I wrote test_services.py (Stage 6) and the extended service tests (Stage 7), reviewed PR #6, ran the Copilot comparison, and wrote parts of the Stage 6, 7, 9 and 12 records. I used an AI assistant to help draft tests and tables, then edited and ran them myself. |
| PG agentic change and rescheduling verification | Not applicable. |
| PG responsible-AI risk/remediation or supported no finding | Not applicable. |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: not undertaken
Separate reflection / peer / common team viva evidence links and routing: The group reflection, confidential peer forms and common team viva evidence are submitted separately through the teaching team's published submission process and are not included in this repository.
No further coding stage. Later corrections use the published assessment process.
