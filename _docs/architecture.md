# Architecture

## Selected stack

The user selected Django after comparing Django and Flask. Use:
- Python 3.11–3.14, within [Django 5.2's supported Python versions](https://docs.djangoproject.com/en/5.2/faq/install/#what-python-version-can-i-use-with-django). Bootstrap was verified with Python 3.12.14; other supported versions are not yet tested here.
- Django 5.2 LTS, pinned to `Django==5.2.18` in `requirements.txt` during bootstrap.
- SQLite for this local academic MVP.
- Django templates and plain CSS for pages.
- Django's built-in authentication, session, password validation, and CSRF facilities.
- Django's built-in test runner and `TestCase`; no extra test framework is required.

Before the bootstrap issue installs dependencies, confirm that the planned patch release can be obtained and pin any justified adjustment in the issue and this document. Do not quietly use an old unsupported release.

References: [supported Django releases](https://www.djangoproject.com/download/), [Django authentication](https://docs.djangoproject.com/en/5.2/topics/auth/default/), and [Django/Flask comparison source](https://flask.palletsprojects.com/en/stable/tutorial/views/).

## Alternatives considered

Django provides standard authentication components and forms that suit a multi-account application. Flask is also possible, but its tutorial assembles the registration and session flow in application views. Django was recommended for this project's account requirement, and the user selected it. SQLite avoids a separate database service for the first version.

## Planned modules

| Path | Responsibility |
| --- | --- |
| `config/` | Settings, root URLs, WSGI/ASGI |
| `accounts/` | Registration and account URLs; reuse Django login/logout facilities |
| `assignments/` | Assignment model, forms, owner-restricted views and URLs |
| `templates/` | Shared layout, account pages, assignment pages |
| `static/css/app.css` | Shared styles |
| `tests/` | Behavioural, ownership, integration, and boundary tests |
| `requirements.txt` | Exact dependency pins |
| `manage.py` | Django commands |

## Assignment model

- `owner`: foreign key to the Django user model, set from the authenticated session.
- `title`: required text, maximum 160 characters after trimming.
- `subject`: required text, maximum 100 characters after trimming.
- `description`: optional plain text, maximum 5000 characters.
- `deadline`: nullable/blank calendar date.
- `is_completed`: boolean, default false.
- `created_at`: creation timestamp used for stable sorting.

These limits are assistant-proposed defaults, documented so implementation and tests agree. The owner is excluded from editable form fields. Use model migrations committed with the issue.

## Time and configuration

Use `TIME_ZONE = "Asia/Almaty"` and `USE_TZ = True` for the initial application. Due dates are calendar dates; overdue means incomplete with a deadline earlier than the local calendar date. Today is not overdue.

Use a development configuration clearly labelled for localhost. Document environment variables for any later production configuration; do not add real secrets to git. The development SQLite file and virtual environment are ignored.
