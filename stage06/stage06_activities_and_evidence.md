# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Tuesday Group 4 (13:30-15:30)
- Members, GitHub usernames and cohorts: (GitHub) AdharvKaimal, kristianreyes13, jesshall902
- Repository URL: https://github.com/AdharvKaimal/st1-assignment-3
- Starting SHA: [response]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Find a registered patient by ID.
- Context: PatientService.find_patient is currently unfinished. It needs to retrieve an existing patient from the shared data store.
- Requirement: FR-02 Patient Search
- Acceptance criteria: 
  - A known patient ID returns the same Patient object stored in the data store.
  
  - IDs are case-sensitive.
  - Blank or non-string IDs raise ValueError.
  - A valid but unknown ID raises LookupError.
  - Searching does not create a replacement patient or change stored records.

- Scope: Implement PatientService.find_patient in services.py and add relevant tests in tests/test_services.py. Use the existing data store validation.
- Definition of Done: All the acceptance criteria are met, testing of new and supplied code are passing with review of another teammate.
- Owner: kristianreyes13
- Actual issue link: [response]

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Cancel a scheduled appointment and retain its history.
- Context: AppointmentService.cancel_appointment is currently unfinished. It needs to cancel an existing scheduled appointment while keeping the appointment in the shared data store.
- Requirement: FR-06 Appointment Cancellation and FR-07 retained history
- Acceptance criteria:
  - Cancelling a SCHEDULED appointment changes its status to CANCELLED.
  - Cancellation returns the same stored Appointment object.
  - The cancelled appointment remains retrievable from the data store.
  - Cancelling an already CANCELLED appointment raises ValueError and leaves its state unchanged.
  - Cancelling a COMPLETED appointment raises ValueError and leaves its state unchanged.
- Scope: Implement AppointmentService.cancel_appointment in services.py and add relevant tests in tests/test_services.py. Use Appointment.cancel() without directly assigning protected state or deleting the appointment.
- Definition of Done: All acceptance criteria are met, new and supplied tests pass. Another team member reviews the changes.
- Owner: kristianreyes13
- Actual issue link: [response]

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|----------------|----------------------------------------------------------------------------------|
| changes | weak | Does not explain what was changed |
| final version | weak | There could be more updates needed and also doesn't really explain what changes. |
| Add patient search by ID | Strong | Clearly shows what changed and what was added |
| fix stuff | Weak | doesn't explain which problem was fixed                                          |
| Prevent cancellation of completed appointments | Strong | Clearly shows what has changed and shows the invalid action that was fixed. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns:  Renaming unrelated patient fields, restructuring unrelated code and adding a new dependency go beyond the cancellation task.
- Responsibility and architecture concerns: Appointment should control cancellation rules, while AppointmentService finds the appointment and calls cancel(). Unrelated changes could disrupt existing responsibilities.
- Testing and review concerns: - Testing and review concerns: Extra changes make the PR harder to review and could introduce bugs that cancellation tests do not cover.
- Changes to remove or separate, with reasons: Keep the cancellation code and relevant tests in this PR. Move justified field renaming, restructuring and dependency changes into separate issues and PRs so they can be tested and reviewed independently.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: Does not explain which requirements, code or tests were checked, or provide anything to show the results
- Follow-up review question 1: Which code changes meet each acceptance criterion?
- Follow-up review question 2: Does cancellation call Appointment.cancel() rather than directly changing the status?
- Follow-up review question 3: Do the tests prove the same appointment object is returned and remains stored after cancellation?
- Follow-up review question 4: Are repeated cancellation and cancellation of completed appointments rejected without changing their state?
- Follow-up review question 5: Are blank, invalid and unknown IDs tested for the correct exceptions?
- Additional questions if useful: What test command was run, from which directory, and what was the actual result? Does the PR contain unrelated changes?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | "Code-{Implementation}" and "stage06-{Author/Editor}" |
| Commit message convention | Standard "Add", "Edit", "Remove", with capitalised operators "AND", "OR", "WITH", "OF", etc. |
| PR size | Limited to Stage Activities and Evidence Document AND project Code (.py) files |
| Another-member review requirement | Peer-review, 1 team member reviews work of work pushed to main. |
| Merge rule | Request made to main repository WITH outlined changes notes. |
| Significant Copilot disclosure rule | All CoPilot (or AI) applications and uses must be disclosed within Push Requests and Commit Notes used when updating the main repository. Additional disclosure is also required if a stage activity permits usage. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [issue 1] | [response] | [response] | [response] | [response] |
| [issue 2] | [response] | [response] | [response] | [response] |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

Commit counts do not provide adequate judgements of contribution or activity by developers, since it measures activity and number of changes regardless of size, rather than actual productivity. Complex and careful implementation of various stages and implementations may take only a few commits, whereas continuous activity produces a large amount of commits. This does not necessarily acknowledge the contribution made by each developer working on the project since work is distributed unevenly across commits.

## L Stage 6 formative questions

1. What is version control?

RESPONSE: Version Control (VC) is a digital software engineering practice of managing and tracking the additions and changes to files in software over time. It is different from a Version Control System (VCS), which is the specific tool used in the development of software manged with Version Control.

2. Why is a feature branch useful?

RESPONSE: The feature of branches in Version Control Systems like GitHub, help to isolate segments of code, usually unfinished or in-development, from the main codebase. This ensures that the main branch or main codebase is stable and bug-free. Branches also enable developers to work in parallel. Additionally, this feature helps developers to submit Push Requests (PRs), which allow discussion and review before changes are merged, which also helps in areas such as code traceability.

3. What makes a commit a good engineering commit?

RESPONSE: A good commit on Version Control System tools like GitHub usually is focused on dealing with one primary issue. This is best practice so that changes can be later reviewed and potentially reversible if needed. A good commit should also have short, descriptive messaging, with an organised and readable format.

4. What is a pull request?

RESPONSE: In a Version Control System, a Pull Request (PR) is a feature allowing individual developers or collaborators to propose changes to the main codebase or project. This system allows developers to work in parallel and also review and discuss changes, edits and implementations to the main codebase of a project.

5. What is the purpose of code review?

RESPONSE: Code reviews are practices in software development that allow teams to identify bugs or defects within a project, improve the quality of the code within the project and also transfer knowledge on the changes and implementations within the program. This practice ensures that code the overal program/software is maintainable and the design of the program is validated.

6. What does a Git diff show?

RESPONSE: Within GitHub, Git diff shows the differences between different states of the respository in a line-by-line sense. This feature also shows additional statistical information, such as the number of lines added, removed, context lines, and the counts of changes in the differing versions of the respository.

7. What is a Definition of Done?

RESPONSE: The Defintion of Done (DoD) is a framework or criteria that determines if a task has been accomplished and is ready for release. This framework is an a common agreement to ensure all work meets agreed-upon standards and quality control before it is deployed or considered finished. This includes aspects like coding, testing, compiling and documentation.

8. What is the appropriate role of GitHub Copilot in pull-request review?

RESPONSE: GitHub Copilot is a basic first-pass reviewer when considering pull-request reviews. However, GitHub Copilot should be limited to this role, as the judgement of human developers determines the overall code reviews and implementation of changes and programming. GitHub Copilot can act to provide potential solutions in terms fo bugs and smaller issues, as well as basic analysis and assessment of code or other changes. However, ultimately, it is up to the human developer to approve changes and exercise reasonable judgement.

9. Why should individual contribution not be judged only by commit count?

RESPONSE: Commit counts do not provide adequate judgements of contribution or activity by developers, since it measures activity and number of changes regardless of size, rather than actual productivity. Complex and careful implementation of various stages and implementations may take only a few commits, whereas continuous activity produces a large amount of commits. This does not necessarily acknowledge the contribution made by each developer working on the project since work is distributed unevenly across commits.

10. What is the Stage 6 engineering rule?

RESPONSE: The principle of collaborative work, communication and creating a character in planning the implementation of a project. This early stage involves the development of agreements between team members, early roles and agreed-upon rules for the project.

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
