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
- The initial dependency pin proposed for bootstrap is Django 5.2.18, based on the official supported-release table checked on 2026-10-12. Confirm package availability at installation.
- Use Django authentication and password hashing.
- Use Django's built-in test runner.
- The backend enforces ownership on every assignment action.
- Local due-date comparisons use Asia/Almaty.
- Follow the article's canonical files plus compatibility entry points for the filenames shown in grading.

## Repository and deadline

- Authenticated GitHub account observed during preparation: `allfocusSS`.
- Project repository: https://github.com/allfocusSS/studytrack (public; provided by the user).
- Course deadline: not supplied.
- Live GitHub issues: [#1](https://github.com/allfocusSS/studytrack/issues/1), [#2](https://github.com/allfocusSS/studytrack/issues/2), [#3](https://github.com/allfocusSS/studytrack/issues/3), [#4](https://github.com/allfocusSS/studytrack/issues/4), [#5](https://github.com/allfocusSS/studytrack/issues/5), [#6](https://github.com/allfocusSS/studytrack/issues/6). Created on 2026-10-12 before implementation.
- Implementation and QA: pending; every issue follows PM → engineer → independent QA.

Replace the missing repository and deadline with the user's actual values. Preserve the history of meaningful decisions; do not invent dates or issue numbers.

## Deferred scope

Group sharing, teacher accounts, email recovery, notifications, attachments, and native mobile applications are outside the initial MVP. If requested later, create linked follow-up issues.
