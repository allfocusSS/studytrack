## Goal

Different students can create independent username/password accounts, log in, and log out through a clear shared interface using Django's account facilities.

## Acceptance criteria

- [ ] Registration at `/accounts/register/` displays username, password, and password confirmation fields without requiring email.
- [ ] A valid new account is saved and the student can log in with its username/password.
- [ ] Registration uses Django's standard user creation form or an equivalent implementation preserving its username rules and default password validators.
- [ ] An existing username produces a readable error and no duplicate account.
- [ ] Missing username/password, invalid username characters, password mismatch, and a password rejected by Django validators produce visible errors without account creation.
- [ ] Passwords are stored using Django's password hashing; the submitted raw password is not stored, logged, or rendered back into the form.
- [ ] `/accounts/login/` authenticates correct credentials and rejects incorrect credentials with a readable error.
- [ ] Successful login creates an authenticated session; a protected test route or equivalent view proves anonymous visitors are redirected to login and logged-in students are allowed.
- [ ] POST `/accounts/logout/` ends the session and redirects to login.
- [ ] GET logout is not a state-changing action and is rejected for a logged-in student.
- [ ] Forms use CSRF protection; a representative account POST without a token is rejected when CSRF enforcement is enabled.
- [ ] The shared `templates/base.html` displays Register/Log in for visitors and username/Logout for signed-in students; assignment navigation is added when those routes exist.
- [ ] The shared stylesheet, visible field labels, readable errors, and keyboard focus follow the design document.
- [ ] Tests cover successful registration, duplicate/invalid input, password hashing, correct/incorrect login, access redirect, logout, and CSRF.
- [ ] The full test suite and Django checks pass. Real results and a tested commit are recorded in the issue, which remains open for QA.

## Out of scope

- Assignment CRUD and assignment navigation before its routes exist — [assignment task](03-assignments.md).
- Shared group lists and teacher roles are outside the MVP.
- Email verification, social login, and automatic email password recovery are outside the MVP.
- Completion and filtering — [status](04-status.md) and [filters](05-filters.md).

Replace draft references with actual issue links after transfer.

## Constraints

- Prerequisite: the [bootstrap task](01-bootstrap.md) is implemented, independently verified, and closed.
- Read `AGENTS.md`, the plan, architecture, testing guidelines, design system, and HTTP contract.
- Files: `accounts/`, `config/urls.py`, relevant settings, account templates, shared `templates/base.html`, `static/css/app.css`, and account tests.
- Reuse Django user/authentication/session/password-validation facilities; do not create a separate password storage scheme.
- Default Django username uniqueness/rules define the initial account contract; tests must state the actual behaviour, including whether differently cased names are treated separately.
- Keep the selected dependency set. Do not introduce a mail provider or unrelated authentication service.
