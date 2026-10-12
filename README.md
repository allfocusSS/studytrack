# StudyTrack

A university assignment tracker with separate student accounts, private task lists, optional descriptions, and optional deadlines.

## Current status

This repository preparation contains the product specification, real brainstorming transcript, selected architecture, agent instructions, initial backlog, and detailed issue drafts.

Application implementation, actual GitHub issue creation, and independent QA are still pending. This is not a completed submission.

## Selected stack

Python + Django 5.2 LTS + SQLite + Django templates + plain CSS.

See [_docs/architecture.md](_docs/architecture.md) for the planned dependency pin and module structure.

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

Repository: https://github.com/allfocusSS/studytrack. The user created this public repository before implementation. Preparation documents and six real issues are being transferred before the first code task. The exact course deadline still needs to be supplied.

PM, engineer, and QA comments must describe work actually performed. Close issues only after QA PASS and before the grading deadline.

## Planned commands after bootstrap

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

```bash
python manage.py test
python manage.py check
python manage.py makemigrations --check --dry-run
```

These commands become executable after the bootstrap issue creates the application and dependency file. The final documentation issue must verify and update them using a fresh clone.
