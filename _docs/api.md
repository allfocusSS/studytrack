# HTTP Routes and Form Contracts

This application serves HTML pages and standard form requests. The MVP does not require a separate JSON API.

| Route | Methods | Access | Behaviour |
| --- | --- | --- | --- |
| `/` | GET | Public | Project home with appropriate account links |
| `/accounts/register/` | GET, POST | Public | Registration form and validation |
| `/accounts/login/` | GET, POST | Public | Login form and authentication |
| `/accounts/logout/` | POST | Signed in | End the session and redirect to login |
| `/assignments/` | GET | Signed in | Private list and filters |
| `/assignments/new/` | GET, POST | Signed in | Create an assignment owned by the current student |
| `/assignments/<pk>/edit/` | GET, POST | Owner | Edit assignment fields |
| `/assignments/<pk>/delete/` | GET, POST | Owner | GET displays confirmation; POST deletes |
| `/assignments/<pk>/status/` | POST | Owner | Set the requested completion state |

All assignment queries are restricted to the current student before a record is retrieved or a form is saved. Another student's ID and a missing ID both return 404 for signed-in students. Unauthenticated protected requests redirect to login.

## Forms

Registration uses username, password, and password confirmation, with Django's default username/password validation and duplicate checks. No email field is required.

Assignment forms expose title, subject, description, and deadline; ownership is never editable. Status is controlled by the status action. Extra crafted owner input never overrides the session's student.

Blank descriptions and deadlines are valid. Dates use ISO `YYYY-MM-DD` in submitted forms. Invalid forms render visible errors and leave stored data unchanged.

The status form submits `is_completed=1` or `is_completed=0`. Other values return a readable 400 error without mutation. Explicit state-setting keeps repeated submissions predictable.

GET on logout or status-changing routes does not mutate data and is rejected as an unsupported method for an authenticated request.

## List query parameters

- `status`: `all`, `pending`, or `completed`; absent or empty means all.
- `subject`: an exact subject value; absent or empty means all subjects.
- Combine both filters using AND.
- An invalid non-empty status produces a readable 400 response and no mutation.
- Subject options come from the current student's assignments only.
- Order by dated entries first, ascending deadline, then ascending creation timestamp and primary key; undated entries follow in stable creation order.

Use CSRF protection for every POST and Django template escaping for user text.
