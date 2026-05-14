# Spec: Add Expenses

## Overview
This step adds the ability for logged-in users to submit new expense entries via a form. It introduces two routes: a `GET` to render the form and a `POST` to validate and persist the data. On success the user is redirected to the dashboard. This is the first write path for the expenses table and is the natural next step after Step 4 made that data visible.

## Depends on
- Step 01 — database setup (expenses table, `get_db()`)
- Step 02 — registration (user accounts exist)
- Step 03 — login/logout (`login_required` decorator, session)
- Step 04 — dashboard (redirect target after successful add)

## Routes
- `GET /expenses/add` — render the add-expense form — logged-in only
- `POST /expenses/add` — validate and insert a new expense, redirect to `/dashboard` — logged-in only

## Database changes
No new tables or columns. One new helper function in `database/db.py`:

- `add_expense(user_id, amount, category, date, description)` — inserts a row into the `expenses` table and returns the new `id`. Uses parameterised `?` placeholders. `description` may be `None`.

## Templates
- **Create:** `templates/add_expense.html` — form page with fields for amount, category, date, and description. Extends `base.html`. Shows validation errors inline when the form is re-rendered after a failed POST.
- **Modify:** none

## Files to change
- `app.py` — implement `GET /expenses/add` and `POST /expenses/add` routes (currently stubs).
- `database/db.py` — add `add_expense()` helper.

## Files to create
- `templates/add_expense.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — never f-strings in SQL
- `login_required` decorator must guard both GET and POST
- Amount must be validated server-side: must be a positive number; reject zero and negative values
- Category must be one of a fixed allowed list (defined in the route, not in JS): `Food`, `Transport`, `Shopping`, `Entertainment`, `Health`, `Bills`, `Other`
- Date must be validated as a real calendar date in `YYYY-MM-DD` format; reject malformed strings
- Date must not be in the future — reject any date after today's date
- Description is optional — treat empty string as `None` before inserting
- On validation failure: re-render `add_expense.html` with the submitted values pre-filled and errors shown above the relevant field
- On success: `flash("Expense added.")` then `redirect(url_for("dashboard"))`
- All templates extend `base.html`
- Use CSS variables — never hardcode hex values
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] Visiting `/expenses/add` while logged out redirects to `/login`
- [ ] Visiting `/expenses/add` while logged in renders a form with fields: Amount, Category (dropdown), Date, Description (optional textarea)
- [ ] Submitting a valid form adds a row to the `expenses` table and redirects to `/dashboard` where the new expense appears
- [ ] Submitting with a missing or non-numeric amount re-renders the form with an error and no DB write occurs
- [ ] Submitting with a zero or negative amount re-renders the form with an error
- [ ] Submitting with an invalid date string re-renders the form with an error
- [ ] Submitting with a future date re-renders the form with an error
- [ ] Submitting with a category not in the allowed list re-renders the form with an error
- [ ] Omitting description saves `NULL` in the DB — no error
- [ ] Previously entered valid field values are pre-filled when the form is re-rendered after a validation error
- [ ] A "Back to Dashboard" link on the form page navigates to `/dashboard`
