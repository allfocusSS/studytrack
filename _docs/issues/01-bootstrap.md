## Goal

Create a reproducible empty StudyTrack Django application with the chosen stack and a passing smoke test, so later features have a verified foundation.

## Acceptance criteria

- [ ] `requirements.txt` pins Django 5.2.18, or the issue documents a verified necessary patch adjustment before implementation.
- [ ] Python compatibility is documented; no unsupported Python/Django combination is used.
- [ ] `manage.py` and `config/` exist, with runnable development settings, root URLs, WSGI, and ASGI modules.
- [ ] Empty `accounts/` and `assignments/` apps are registered without account or assignment product features.
- [ ] SQLite is the development database; no separate database service is required.
- [ ] An anonymous GET to `/` returns 200 and a minimal response identifying StudyTrack.
- [ ] At least one meaningful Django smoke test asserts the real root route's status and application identifier.
- [ ] `python manage.py migrate` succeeds on a clean temporary development database.
- [ ] `python manage.py test` passes and discovers the smoke test.
- [ ] `python manage.py check` reports no system errors.
- [ ] `python manage.py makemigrations --check --dry-run` reports no missing migrations.
- [ ] README contains the bootstrap commands, verified in a new virtual environment; later feature commands are not presented as completed features.
- [ ] The virtual environment, local database, and real credentials are ignored by git and are not included in the commit.
- [ ] Implementation is committed, with actual command results posted in the live issue; the engineer leaves it open for independent QA.

## Out of scope

- Registration/login/logout — [account task](02-accounts.md).
- Assignment model and CRUD — [assignment task](03-assignments.md).
- Completion/overdue behaviour and filters — [status](04-status.md) and [filters](05-filters.md).
- Final integration evidence — [integration task](06-integration.md).
- Production deployment and additional frameworks are outside the planned MVP.

These are initial draft references; replace them with actual issue links when transferred.

## Constraints

- This is the first implementation task. It starts only after live issue creation and PM grooming.
- Follow `AGENTS.md`, `_docs/architecture.md`, `_docs/process.md`, and `_docs/testing-guidelines.md`.
- Scope: `requirements.txt`, `manage.py`, `config/`, empty app scaffolds, `tests/`, README, and relevant dependency/version decisions.
- Use Django's built-in test runner. No extra test framework, REST framework, React, or external database.
- The initial pin comes from the supported-release table; confirm actual installation availability and report any discrepancy instead of silently substituting a release.
- This draft describes future work; no tests or implementation are claimed to have run.
