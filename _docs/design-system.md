# Design System

## UI principles

Use English interface labels, clear forms, and a responsive single-column layout on narrow screens. Avoid extra product features or implementation terminology on user-facing pages.

## Shared layout

Every page extends `templates/base.html`. Signed-out navigation shows Register and Log in. Signed-in navigation shows My assignments, Add assignment, the current username, and a POST Logout form.

## Styles

Use one stylesheet: `static/css/app.css`.

- Background: `#f4f7fb`.
- Text: `#182230`.
- Primary action: `#2457d6` with white text.
- Surfaces: white with a subtle border.
- Errors/overdue: red text plus a readable text label; colour alone is insufficient.
- Completed state: a text badge labelled Completed.

Keep named reusable classes for buttons, panels, form fields, errors, and assignment cards.

## Forms and lists

Each input has a visible associated label. Required fields are identified. Description and deadline are explicitly labelled optional. Deadline controls accept a calendar date and can be cleared.

Errors appear next to the relevant field or as a readable form error. Preserve non-password input after validation failures. Passwords are never repopulated into the HTML form.

Assignments display title, subject, description when present, a formatted deadline or No deadline, status, and owner-appropriate controls.

Deletion uses a confirmation screen with Cancel and Delete actions. An empty list offers Add assignment; a filtered empty result offers Clear filters.

## Accessibility and layout

Support keyboard navigation, visible focus, semantic headings, and labelled controls. At approximately 375px and 1280px viewport widths, essential content remains readable and actions usable without horizontal page scrolling.
