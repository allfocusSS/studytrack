# StudyTrack — Product Specification

## 1. Purpose

StudyTrack is a small web application that helps students keep track of their university assignments. Each student has a separate account and a private list of assignments.

The first version focuses on assignment management. This product specification was prepared before stack selection and implementation. The user has now selected Django; technical decisions are recorded in `_docs/architecture.md` and `_docs/decisions.md`.

## 2. Decisions confirmed in the brainstorming chat

- There are accounts for different students.
- Students register and sign in using a username and password, without an email address.
- Each student can see and change only their own assignments.
- An assignment has a title, subject, deadline, and completion status.
- An assignment also has an optional description.
- The deadline is optional. An assignment can be created without a date, and a date can be added later.
- A username must be unique. An already-used username produces a readable validation error.

The project idea and the title, subject, deadline, and status fields were proposed by the assistant and used as the basis of the subsequent scope questions. The user's answers are preserved in `chat-brainstrom.md`.

## 3. MVP defaults

The following details complete the MVP specification. They are implementation defaults proposed by the assistant, rather than additional answers attributed to the user:

- Students can register, log in, and log out.
- Students can create, list, edit, and delete their own assignments.
- Students can mark an assignment completed and return it to not completed.
- New assignments start as not completed.
- The title and subject are required after surrounding whitespace is removed.
- Descriptions can be empty.
- Deadlines are calendar dates, without a time of day.
- A valid past deadline is allowed. An incomplete assignment with a past deadline is shown as overdue.
- Completed assignments and assignments without a deadline are not overdue.
- The list can be filtered by subject and by status: all, not completed, or completed.
- Dated assignments are ordered by the nearest deadline first; assignments without a date appear after them. Ties use a stable creation order.
- The first version uses a simple, responsive interface with English labels.

## 4. Assignment data

| Field | Required? | Behaviour |
| --- | --- | --- |
| Owner | Set by the application | Always the signed-in student; never selected from the form |
| Title | Yes | A short, non-blank assignment name |
| Subject | Yes | A non-blank subject name entered as text |
| Description | No | Plain text; an empty value is allowed |
| Deadline | No | A valid calendar date or an empty value |
| Status | Yes, with a default | Not completed by default; can be changed to completed |

Usernames and passwords are account data and are not assignment fields. Detailed input lengths and password validation will be specified when the chosen framework is documented and the authentication issue is groomed.

## 5. Screens and user flow

1. A visitor opens the application and sees links to register or log in.
2. Registration asks for a username, a password, and password confirmation.
3. After registering, the student can log in and open their assignment list.
4. An empty list shows a clear message and an option to add the first assignment.
5. The creation form collects the assignment fields and accepts an empty description and deadline.
6. The student returns to the list after saving an assignment.
7. The student can edit it, change its completion status, or delete it after confirmation.
8. Logging out ends the session and returns the student to the login screen.

Invalid input displays readable errors without creating a partial record or losing the other form values.

## 6. Access and account rules

- Registration and login are available to visitors.
- Assignment pages and all assignment actions require a signed-in student.
- The server checks ownership for every read, edit, status change, and deletion.
- Knowing another student's assignment ID or URL never grants access.
- Requests for another student's assignment return a not-found response and do not reveal its contents or modify it.
- Every list query is restricted to the current student's assignments, including filtered queries.
- Passwords must use the selected framework's password hashing facilities; raw passwords must not be stored or logged.
- Use the framework's session and form protection features. A delete or other state-changing action must not be performed by a GET request.
- An incorrect username/password combination displays a readable login error.
- Logout invalidates the active session.

Hiding another student's assignments in the interface alone is not sufficient; these rules must be enforced by the server.

## 7. Acceptance scenarios

| Scenario | Expected result |
| --- | --- |
| Register with a new valid username | An account is created and the student can log in |
| Register with an existing username | A readable error appears; no duplicate account is created |
| Enter an incorrect password | Login fails and no authenticated session is created |
| Open assignment pages without logging in | The visitor is directed to log in |
| Create a valid assignment without a deadline | It is saved and shown with a clear no-deadline label |
| Add a deadline to an existing undated assignment | The date is saved and displayed on the list |
| Clear an existing deadline | The assignment becomes undated again |
| Leave the description empty | The assignment can still be saved |
| Submit a blank title or subject | A readable error appears; no invalid assignment is saved |
| Submit an invalid date | A readable error appears; the saved assignment remains unchanged |
| Edit an assignment | The updated values appear and persist after reloading |
| Mark an assignment completed, then not completed | Both changes persist and the status filter reflects them |
| Cancel deletion | The assignment remains present |
| Confirm deletion | Only that student's selected assignment is removed |
| Use a subject or status filter | Only the current student's matching assignments appear |
| No assignments match the filter | A clear empty-result message appears |
| Student B requests student A's assignment URL or sends an update/delete request | A not-found response is returned; A's record remains unchanged |
| Restart the application | Saved accounts and assignments remain available |
| Log out and try a protected action | The previous session cannot perform the action |

These product scenarios will be divided into small GitHub issues. QA will report actual results against each issue's acceptance criteria.

## 8. Out of scope for the first version

- Shared group lists and assignment sharing.
- Teacher or group-administrator accounts.
- Email login, email verification, and automated email password recovery.
- Email or push deadline reminders.
- File attachments.
- AI-generated assignments or summaries.
- A native mobile application.
- Production deployment as a prerequisite for this initial MVP.

These are scope boundaries proposed for the MVP. If a deferred feature becomes required, create a follow-up issue and link it from the relevant issue rather than silently dropping work.

## 9. Development workflow and submission evidence

1. Preserve the real brainstorming conversation in `chat-brainstrom.md`.
2. Save this product specification as `_docs/plan.md`.
3. Compare technology options, choose a stack, and document the decision.
4. Create a small initial backlog in `_docs/tasks.md`; its first task sets up an empty project with a passing test.
5. Create a public GitHub repository and move the backlog into real GitHub issues.
6. Once transferred, GitHub issues become the only active backlog. Keep `tasks.md` as a clearly labelled historical snapshot if it is retained for grading.
7. Add `AGENTS.md`, the process, the issue template, role instructions, and relevant testing/design/API documents.
8. Work through one issue at a time: PM grooming, engineer implementation, then independent QA.
9. If QA reports FAIL, return to the engineer and repeat QA after the fix.
10. Close an issue only after QA reports PASS. Record implementation and QA evidence in its comments, with actual test commands and results.
11. Commit meaningful changes and push the source and documentation to GitHub.
12. Submit the repository link.

The assignment spells the transcript filename as `chat-brainstrom`, so that spelling is intentionally used. The article uses `AGENTS.md` and `_docs/team/`; compatibility documents at `AGENT.md` and `roles/` can point to the canonical files to cover the grading examples without creating conflicting instructions.

## 10. Current state and remaining decisions

- Product brainstorming: completed in this conversation.
- Technology stack: Django + SQLite selected by the user after comparing Django and Flask.
- Agent/process/role documentation and six detailed issue drafts: prepared locally.
- Public GitHub repository: https://github.com/allfocusSS/studytrack, created by the user.
- GitHub issues: six live issues created before implementation; links in `_docs/issues/index.md`.
- Application code and automated tests: not implemented yet.
- Issue implementation and QA: not performed yet.
- Course deadline: not supplied. Record the exact deadline and timezone before starting the issue workflow; counted issues must be opened and closed before it.

This document describes intended behaviour. It does not claim that the application has already been built or tested.

