# Initial Backlog

Status: historical initial backlog, transferred to GitHub on 2026-10-12. GitHub issues are the only active backlog. These descriptions record the original decomposition before live PM grooming.

Actual issue links are in [_docs/issues/index.md](issues/index.md). Read the live issues for current criteria, not these historical drafts.

## 1. Bootstrap Django with a passing test
Goal: A reproducible empty Django application starts and has a passing smoke test.
Description: Set up the selected Django/SQLite stack, basic modules and a minimal home response. Pin dependencies and document the initial commands; do not implement accounts or assignment features.
Draft: [01-bootstrap.md](issues/01-bootstrap.md).

## 2. Student registration, login, and logout
Goal: Students have independent accounts and authenticated navigation.
Description: Implement username/password registration using Django account facilities, validation, login, POST logout, and a shared page layout. Preserve meaningful authentication errors and cover the account lifecycle.
Prerequisite: task 1.
Draft: [02-accounts.md](issues/02-accounts.md).

## 3. Private assignment CRUD and optional fields
Goal: Students can create, read, edit, and delete their own assignments.
Description: Add the owner-bound model, forms, personal list and CRUD routes. Support optional description/deadline, required title/subject, validation, delete confirmation, and server-side ownership checks.
Prerequisite: task 2.
Draft: [03-assignments.md](issues/03-assignments.md).

## 4. Completion status and overdue behaviour
Goal: Students can complete or reopen an assignment and see accurate overdue labels.
Description: Add a protected POST action that sets completion status. Compute overdue from an optional deadline and local date, with tests around today, completed entries, and undated entries.
Prerequisite: task 3.
Draft: [04-status.md](issues/04-status.md).

## 5. Subject/status filters and deterministic ordering
Goal: Students can focus their private list and see predictable deadline ordering.
Description: Add subject and status filters with combined behaviour, empty-result handling, and dated-first sorting. Keep subject choices and query results restricted to the current student's data.
Prerequisite: task 4.
Draft: [05-filters.md](issues/05-filters.md).

## 6. Integrated verification and submission documentation
Goal: A fresh clone can run the documented MVP and the submission evidence is complete.
Description: Verify the full two-account scenario, responsive pages, system/migration checks, and accurate launch/test instructions. Record actual evidence and reconcile documentation with the implemented application.
Prerequisites: tasks 1–5.
Draft: [06-integration.md](issues/06-integration.md).
