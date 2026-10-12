## Goal

Students can mark their own assignments completed or not completed, and the interface identifies overdue work correctly even when a deadline is missing.

## Acceptance criteria

- [ ] POST `/assignments/<pk>/status/` accepts `is_completed=1` and stores completed=true for an owned assignment.
- [ ] The same action accepts `is_completed=0` and stores completed=false.
- [ ] Repeating a request with the same desired state keeps that state; it does not accidentally toggle twice.
- [ ] Any other/missing status value produces a readable 400 error without changing the record.
- [ ] The list provides a clear complete/reopen control appropriate to the current status, and the result persists after reload.
- [ ] GET to the status action does not change data and is rejected for a signed-in student.
- [ ] Anonymous status requests redirect to login without mutation.
- [ ] Another student's assignment ID returns 404 for status requests and that record remains unchanged.
- [ ] The status form is CSRF protected; a missing token is rejected when enforcement is enabled.
- [ ] Overdue means not completed with a deadline earlier than the current local date in Asia/Almaty.
- [ ] An incomplete assignment due today is not overdue.
- [ ] An incomplete assignment due in the future is not overdue.
- [ ] An assignment without a deadline is not overdue.
- [ ] A completed assignment with a past deadline is not overdue.
- [ ] Reopening a completed past-due assignment makes its overdue label appear.
- [ ] Overdue and completed states have readable text labels; colour alone is not used to convey them.
- [ ] Tests control the local date and cover every boundary above, both status transitions, repeated submissions, invalid values, CSRF, and ownership.
- [ ] The full suite and Django checks pass; the implementation comment identifies the actual tested commit and observed results.

## Out of scope

- Filtering or list sorting — [filter task](05-filters.md).
- CRUD fields and validation are supplied by [assignment task](03-assignments.md).
- Reminders, emails, recurring assignments, and group access are outside the MVP.

Replace draft references with actual issue links after transfer.

## Constraints

- Prerequisite: the [assignment task](03-assignments.md) is independently verified and closed.
- Files: assignment views/URLs, model-derived overdue behaviour as needed, list template/styles, and status/date tests.
- Follow `_docs/api.md` and the documented local-date rule.
- Keep deadline a nullable calendar date; no time-of-day field or scheduled job.
- Do not trust a submitted owner or accept an arbitrary model field as the status value.
- Keep all existing assignment permission tests passing.
