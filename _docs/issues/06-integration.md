## Goal

The complete MVP works from a fresh checkout, its interface is usable, and the repository provides truthful, complete development and grading evidence.

## Acceptance criteria

**Integrated behaviour**

- [ ] A fresh virtual environment can install the pinned requirements, run migrations, start the app, and run the complete suite using README.
- [ ] Two students can register and log in independently using usernames/passwords without email.
- [ ] Student A can create an assignment with no description or deadline, add a date later, clear it again, complete/reopen it, and delete it after confirmation.
- [ ] Student B cannot list A's assignments or read/edit/delete/change their status using direct URLs or crafted requests.
- [ ] The walkthrough covers duplicate username errors, invalid assignment input, optional fields, overdue boundaries, filters, sorting, deletion cancellation, and logout.
- [ ] Saved test accounts/assignments persist after restarting a disposable development instance.
- [ ] The primary account and assignment pages are inspected at approximately 375px and 1280px widths with actual observations recorded.
- [ ] Labels, errors, keyboard focus, and essential controls are usable without horizontal page scrolling.
- [ ] At least one end-to-end behavioural test covers the multi-step two-account workflow.

**Checks and documentation**

- [ ] `python manage.py test`, `python manage.py check`, and `python manage.py makemigrations --check --dry-run` pass on the final reviewed commit, with actual results.
- [ ] README accurately documents prerequisites, installation, migrations, launch, tests, implemented features, and known limitations.
- [ ] The plan, architecture, route document, testing guidelines, design document, and agent commands agree with the running application.
- [ ] The real transcript is preserved, including the Django selection, without invented conversation messages.
- [ ] The required canonical Markdown files and compatibility entry points exist and their local links resolve.
- [ ] The historical task list and draft index link to actual live GitHub issues and do not claim to be the active backlog.
- [ ] The submission checklist records the real repository URL and course deadline; completed checkboxes have evidence.
- [ ] No environment, personal development database, credentials, or private session data is committed.
- [ ] The engineer posts actual implementation/check results and leaves the issue open for independent QA. The orchestrator closes it only after PASS and successful push.

## Out of scope

- New product features or a redesign.
- Public hosting is outside the initial academic MVP.
- Repairing a newly discovered defect inside a different issue without documenting the handoff. A FAIL returns to the responsible engineer; create and link a follow-up issue if separate work is required.
- Claims that GitHub issue timestamps or results can be backdated.

## Constraints

- Prerequisites: the preceding [bootstrap](01-bootstrap.md), [accounts](02-accounts.md), [assignment](03-assignments.md), [status](04-status.md), and [filter](05-filters.md) tasks are independently verified and closed.
- Scope: integration tests and accurate documentation. Product fixes require a clear issue/engineer handoff.
- QA is a separate subagent and reports findings without changing implementation.
- Every counted live issue, including this one, must be opened and closed before the actual deadline.
- Never mark a criterion PASS based only on an engineer's statement or an unrun command.
- Replace these local draft prerequisites with actual issue links after transfer.
