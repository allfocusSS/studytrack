## Goal

A signed-in student can create, list, edit, and delete private assignments, with optional descriptions and optional deadlines. Every operation enforces ownership on the server.

## Acceptance criteria

**Model and validation**

- [ ] An Assignment model stores owner, title, subject, description, nullable deadline, is_completed defaulting to false, and created_at.
- [ ] A committed migration creates the model on a fresh database.
- [ ] Owner is assigned from the current authenticated student and excluded from editable form fields.
- [ ] Title and subject are required after trimming surrounding whitespace.
- [ ] Title length is at most 160 characters, subject at most 100, and description at most 5000; boundary values succeed and excessive values show errors.
- [ ] An empty description is accepted.
- [ ] An empty deadline is accepted and stored as null.
- [ ] Valid past, today, and future dates are accepted. Malformed dates produce visible errors without creating or changing stored data.
- [ ] New assignments are not completed.

**Own-assignment workflow**

- [ ] `/assignments/` lists only the signed-in student's assignments.
- [ ] The list displays title, subject, non-empty description, a deadline or No deadline, and a clear completion status.
- [ ] A student with no assignments sees a readable empty state and an Add assignment action.
- [ ] GET/POST `/assignments/new/` supports a valid form and returns the student to the list after saving.
- [ ] Editing changes only the selected owned assignment, with previous values prefilled.
- [ ] Editing supports adding a deadline to an undated assignment, changing it, and clearing it back to null.
- [ ] Failed creation/edit validation displays field errors and preserves non-password input; existing data remains unchanged.
- [ ] GET delete shows confirmation without deleting. Cancel returns to the list and preserves the record.
- [ ] POST confirmation removes only the selected owned assignment.
- [ ] Navigation links point to existing routes and all pages use the shared layout.

**Ownership and protection**

- [ ] Unauthenticated list/create/edit/delete requests redirect to login and cause no mutation.
- [ ] Student B receives 404 for student A's edit and delete URLs, including crafted POST requests; A's assignment remains unchanged.
- [ ] A crafted owner value on creation/edit never transfers ownership or creates an assignment for another student.
- [ ] Missing assignment IDs return a not-found response.
- [ ] All mutating forms use CSRF protection and GET requests never create/edit/delete a record.
- [ ] User-provided titles, subjects, and descriptions are escaped when rendered.

**Done means**

- [ ] Tests cover CRUD, validation boundaries, optional fields, deadline changes, ownership denial with unchanged database assertions, and HTML escaping.
- [ ] SQLite persistence survives application restart, verified against a disposable database.
- [ ] The full suite, system checks, and migration consistency check pass with real evidence in the live issue.

## Out of scope

- Setting completion status after creation and overdue labels — [status task](04-status.md).
- Filtering and specified deadline ordering — [filter task](05-filters.md).
- Accounts are supplied by the [account task](02-accounts.md); do not redesign them.
- Sharing, attachments, notifications, and teacher accounts are outside the MVP.

Replace draft references with actual issue links after transfer.

## Constraints

- Prerequisite: the [account task](02-accounts.md) is independently verified and closed.
- Files: `assignments/`, its migration, assignment templates, `config/urls.py`, relevant navigation/styles, and assignment tests.
- Follow the plan, architecture, design, route contracts, and testing guidelines.
- Use an owner-restricted queryset before fetching an object; never fetch another student's object and merely hide it in the template.
- Use Django forms/ORM. No additional dependency or separate subject-management feature.
- Build the boolean status field now to support the later status task, but do not implement that task's action prematurely.
