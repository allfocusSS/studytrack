# Testing Guidelines

## Commands

After bootstrap, use `python manage.py test`, `python manage.py check`, and `python manage.py makemigrations --check --dry-run`.

Record real commands and results in implementation/QA comments. Do not use claimed or estimated counts.

## Approach

Use Django `TestCase` and the test client for behaviour, with isolated test database data. Keep tests deterministic and focused on outcomes rather than matching implementation details.

Use two independent students in ownership tests. Check the database after denied writes; a response code by itself does not prove another student's data remained unchanged.

## Required coverage

- Registration success, duplicate usernames, missing fields, mismatched passwords, and framework password validation.
- Correct login, wrong credentials, logout, and unauthenticated access.
- Required title/subject trimming and empty input, documented maximum lengths, optional descriptions.
- Blank, valid, invalid, past, today, and future deadlines.
- Adding, changing, and clearing a saved deadline.
- Create/read/edit/delete and completion/reopening behaviour.
- Ownership on listing, editing, deletion, and status changes, including crafted owner values.
- Filters and deterministic ordering, including undated assignments.
- Empty lists and empty filtered results.
- CSRF enforcement on at least one representative mutating endpoint.
- Escaping user text in rendered HTML.

Tests for overdue dates must control the local date instead of assuming the day the suite runs.

## Manual QA

When the issue concerns UI, inspect the actual page at a desktop width and a narrow mobile width. Verify labels, visible errors, keyboard focus, and that essential controls remain usable without horizontal page scrolling. Record only checks actually performed.

The final walkthrough uses two real test accounts and demonstrates private data, an undated assignment, editing, status filters, deadline changes, deletion cancellation, and logout.

## Test data

Use disposable accounts and temporary test databases. Do not commit a personal development database or real passwords.
