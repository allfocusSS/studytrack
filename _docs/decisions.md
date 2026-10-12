# Decisions

## Confirmed product choices

1. StudyTrack is a web application for tracking university assignments.
2. Different students have separate accounts.
3. Accounts use a unique username and password.
4. Each student has a private assignment list.
5. Descriptions are optional.
6. Deadlines are optional and can be added, removed, or changed later.
7. The user selected Django after the framework comparison.

The real conversation is preserved in `chat-brainstrom.md`. Product defaults that were not separate user answers are identified in `plan.md`.

## Technical defaults

- Django 5.2 LTS + SQLite + Django templates + plain CSS.
- The dependency pin is `Django==5.2.18`, based on the official supported-release table checked on 2026-10-12. Bootstrap installation was verified on Python 3.12.14 in a new virtual environment; no patch adjustment was needed.
- Use Django authentication and password hashing.
- Use Django's built-in test runner.
- The backend enforces ownership on every assignment action.
- Local due-date comparisons use Asia/Almaty.
- Follow the article's canonical files plus compatibility entry points for the filenames shown in grading.

## Repository and deadline

- Authenticated GitHub account observed during preparation: `allfocusSS`.
- Project repository: https://github.com/allfocusSS/studytrack (public; provided by the user).
- Course deadline displayed by the user-supplied Moodle screenshot: **Tuesday, 13 October 2026, 14:30**. The screenshot does not show a timezone. For planning only, assume **Asia/Almaty (UTC+05:00)**, corresponding to `2026-10-13T09:30:00Z`; this is an explicit assumption, not a timezone confirmed by the screenshot. The authoritative deadline is the time displayed by Moodle.
- Live GitHub issues: [#1](https://github.com/allfocusSS/studytrack/issues/1), [#2](https://github.com/allfocusSS/studytrack/issues/2), [#3](https://github.com/allfocusSS/studytrack/issues/3), [#4](https://github.com/allfocusSS/studytrack/issues/4), [#5](https://github.com/allfocusSS/studytrack/issues/5), [#6](https://github.com/allfocusSS/studytrack/issues/6). Created on 2026-10-12 before implementation.
- Bootstrap #1: implemented and engineer-tested locally; independent QA and publication remain pending. Feature issues #2–#6 remain pending. Every issue follows PM → engineer → independent QA.

Both issue creation and closure must precede the course deadline. Preserve real GitHub timestamps; do not claim confirmed timezone or final deadline compliance until the evidence supports it.

## Deferred scope

Group sharing, teacher accounts, email recovery, notifications, attachments, and native mobile applications are outside the initial MVP. If requested later, create linked follow-up issues.
