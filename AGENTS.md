# StudyTrack — Agent Instructions

## Product and stack

Read [_docs/plan.md](_docs/plan.md) before changing product behaviour. Students have separate username/password accounts, private assignments, optional descriptions, and optional deadlines.

The selected stack is Python, Django 5.2 LTS, SQLite, Django templates, and plain CSS. Read [_docs/architecture.md](_docs/architecture.md) and [_docs/decisions.md](_docs/decisions.md).

## Commands

These commands apply after the bootstrap issue creates the application:
- `python3 -m venv .venv`: create a development environment.
- `source .venv/bin/activate`: activate it on macOS/Linux.
- `python -m pip install -r requirements.txt`: install pinned dependencies.
- `python manage.py migrate`: prepare the local SQLite database.
- `python manage.py runserver`: run the local application.
- `python manage.py test`: run the complete test suite.
- `python manage.py check`: run Django's system checks.
- `python manage.py makemigrations --check --dry-run`: check for missing migrations.

## Documents

- [_docs/process.md](_docs/process.md): the required issue lifecycle and orchestrator rules.
- [_docs/task-template.md](_docs/task-template.md): issue specification format.
- [_docs/team/pm.md](_docs/team/pm.md): PM role.
- [_docs/team/software-engineer.md](_docs/team/software-engineer.md): engineer role.
- [_docs/team/qa-engineer.md](_docs/team/qa-engineer.md): QA role.
- [_docs/testing-guidelines.md](_docs/testing-guidelines.md): read before writing or evaluating tests.
- [_docs/design-system.md](_docs/design-system.md): read before changing UI.
- [_docs/api.md](_docs/api.md): routes, request methods, and access rules.
- [_docs/tasks.md](_docs/tasks.md): initial backlog; historical reference after transfer.
- [_docs/submission-checklist.md](_docs/submission-checklist.md): grading evidence and deadline checks.

## Working rules

- The main session is the orchestrator. It must launch separate PM, software-engineer, and QA subagents, using the corresponding role instructions, for the issue lifecycle. It does not groom, implement, or judge its own implementation.
- Work through one live GitHub issue at a time, in dependency order.
- Read acceptance criteria before work and again before handing it over.
- The engineer never closes an issue. QA reports findings without fixing code. Only the orchestrator closes an issue after independent QA PASS and a successful push.
- Enforce assignment ownership on the server; UI hiding is insufficient.
- Use Django authentication, sessions, password hashing, and CSRF protection.
- Pin dependencies in `requirements.txt`. Django is selected; do not add optional frameworks or unrelated services without a documented reason and an issue covering the change.
- Commit meaningful changes regularly; include the real issue number in implementation commits.
- Do not invent test runs, issue numbers, issue timestamps, comments, approvals, or PASS results.
- Never include a development database, raw passwords, session cookies, credentials, or generated environments in the repository.
- GitHub issues become the only active backlog when the local drafts have been transferred. Do not treat draft files as proof that live issues exist.
