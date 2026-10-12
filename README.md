# StudyTrack

A university assignment tracker being built with separate student accounts, private task lists, optional descriptions, and optional deadlines.

## Current status

The bootstrap application serves a minimal public `StudyTrack` response at `/`, uses SQLite, and includes a root-route smoke test. Empty `accounts` and `assignments` apps are registered; registration, login/logout, and assignment features are forthcoming in [issues #2–#6](https://github.com/allfocusSS/studytrack/issues).

Six [live GitHub issues](https://github.com/allfocusSS/studytrack/issues) were created before implementation. Their comments record implementation and independent QA evidence. The complete MVP and final submission evidence are still pending.

## Selected stack

Python + Django 5.2 LTS + SQLite + Django templates + plain CSS.

`requirements.txt` pins Django to `5.2.18`. See [_docs/architecture.md](_docs/architecture.md) for the module structure.

## Python prerequisites

StudyTrack supports **Python 3.11–3.14**, within the versions in [Django 5.2's Python compatibility table](https://docs.djangoproject.com/en/5.2/faq/install/#what-python-version-can-i-use-with-django). Bootstrap verification used **Python 3.12.14** with Django **5.2.18**. Other supported Python versions have not yet been tested here.

Use a Python installation with `venv`, `pip`, and the built-in `sqlite3` module available. Dependency installation requires access to a Python package index; no separate database or web server is required.

## Local setup

Run these commands from the repository root on macOS/Linux. `python3` must select a supported Python version.

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -r requirements.txt
python -m django --version
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ to see `StudyTrack`. Stop the development server with Ctrl+C before running more commands in the same terminal. `migrate` creates a local `db.sqlite3` with Django's standard tables; an anonymous request to `/` needs no accounts or existing rows.

These are **local development settings**: debug mode is enabled, allowed hosts are localhost/127.0.0.1/IPv6 loopback, and the checked-in secret key is an explicitly public development placeholder. Production configuration is outside this bootstrap. Local databases, virtual environments, and local credential files are ignored by git.

## Verification

With the virtual environment active, run:

```bash
python manage.py test
python manage.py check
python manage.py makemigrations --check --dry-run
```

The bootstrap commands were verified in an isolated working copy with no existing virtual environment or database, using a new virtual environment on Python 3.12.14. Dependency installation and 18 standard Django migrations succeeded. The test command discovered and passed one root-route smoke test, system checks found no issues, and the missing-migration check reported no changes. Actual HTTP requests to the running server at http://127.0.0.1:8000/ and http://localhost:8000/ returned 200 with `StudyTrack`; the temporary server was then stopped. Exact commands and observed results are recorded on [issue #1](https://github.com/allfocusSS/studytrack/issues/1); independent QA is a separate step in the issue workflow.

## Documents

- [Brainstorming transcript](chat-brainstrom.md).
- [Product specification](_docs/plan.md).
- [Agent instructions](AGENTS.md).
- [Process](_docs/process.md).
- [Initial backlog](_docs/tasks.md).
- [Draft issues](_docs/issues/index.md).
- [Submission checklist](_docs/submission-checklist.md).

The singular `AGENT.md`, root `process.md`, and `roles/` files are compatibility entry points to the canonical instructions.

## Repository and workflow

Repository: https://github.com/allfocusSS/studytrack. The user created this public repository before implementation. Preparation documents are published, and six real issues were created before the first code task. The Moodle screenshot displays a deadline of 13 October 2026 at 14:30 without a timezone; [_docs/decisions.md](_docs/decisions.md) records the explicit Asia/Almaty planning assumption.

PM, engineer, and QA comments must describe work actually performed. Close issues only after QA PASS and before the grading deadline.
