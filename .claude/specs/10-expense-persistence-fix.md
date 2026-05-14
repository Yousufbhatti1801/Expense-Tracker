# Spec: Expense Persistence Fix

## Overview
Steps 1–9 left one gap in the expense CRUD lifecycle: users cannot edit an expense once it is saved. This step closes that gap by implementing the edit expense route, two new DB helpers (`get_expense_by_id` and `update_expense`), and an edit form template. It also ensures ownership is enforced at every layer — the fetch, the render, and the update — so no user can view or modify another user's data. The "fix" framing reflects that the stub route listed in CLAUDE.md (`GET /expenses/<id>/edit`) has been an open hole in the feature surface since Step 5.

## Depends on
- Step 1 — database schema (`expenses` table, `get_db()`, FK pragma)
- Step 3 — `login_required` decorator (must guard both GET and POST)
- Step 4 — dashboard that lists expenses (entry point to the edit link)
- Step 5 — add expense route (validation rules and form structure to reuse)
- Step 7 — delete expense (ownership-scoped WHERE clause pattern to follow)

## Routes
- `GET /expenses/<int:expense_id>/edit` — render pre-filled edit form for the given expense — logged-in only
- `POST /expenses/<int:expense_id>/edit` — validate submitted data, persist the update, redirect to dashboard — logged-in only

## Database changes
No new tables or columns. Two new helper functions added to `database/db.py`:

**`get_expense_by_id(expense_id, user_id)`**
- `SELECT * FROM expenses WHERE id = ? AND user_id = ?`
- Returns a single `sqlite3.Row` or `None` if not found / not owned by user

**`update_expense(expense_id, user_id, amount, category, date, description)`**
- `UPDATE expenses SET amount = ?, category = ?, date = ?, description = ? WHERE id = ? AND user_id = ?`
- Ownership scoped in the WHERE clause — not just application-layer
- Returns `True` if a row was updated, `False` otherwise
- Must not touch `created_at`

## Templates
- **Create:** `templates/edit_expense.html` — mirrors `add_expense.html` in field set (amount, category dropdown, date, description); pre-fills each field from the fetched expense row; submit button labelled "Update Expense"; form action points to `url_for('edit_expense_view', expense_id=expense.id)` with `method="POST"`; displays inline validation errors on re-render; extends `base.html`
- **Modify:** `templates/dashboard.html` — add an "Edit" link/button per expense row pointing to `url_for('edit_expense_view', expense_id=expense['id'])`; place it adjacent to the existing Delete button

## Files to change
- `database/db.py` — add `get_expense_by_id()` and `update_expense()` helpers
- `app.py` — implement `edit_expense_view()` (handles GET and POST); import the two new helpers; add the route decorator
- `templates/dashboard.html` — add Edit link per row in the expense table
- `CLAUDE.md` — update the routes table: mark `GET /expenses/<id>/edit` as Implemented — Step 10

## Files to create
- `templates/edit_expense.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — `?` placeholders in all SQL; never f-strings or string concatenation in queries
- Passwords hashed with werkzeug (not applicable here, but rule stands)
- Use CSS variables — never hardcode hex values in any template or stylesheet
- All templates extend `base.html`
- `get_expense_by_id()` must include `user_id` in its WHERE clause — fetching by ID alone is forbidden
- `update_expense()` must include `user_id` in its WHERE clause — application-layer ownership checks are not sufficient
- If `get_expense_by_id()` returns `None` on GET, call `abort(404)` — do not return a plain string
- Validation on POST must be identical to the add expense flow:
  - Amount: valid positive float, not zero or negative
  - Category: must be one of the seven values in `EXPENSE_CATEGORIES`
  - Date: YYYY-MM-DD format, must not be in the future
  - Description: optional — store `None` if blank, not an empty string
- On validation failure: re-render `edit_expense.html` with error messages and the user's submitted values preserved
- On success: flash a confirmation message (e.g. "Expense updated.") and `redirect(url_for('dashboard'))`
- `created_at` must never be touched by the update query or the route function
- Apply the `@login_required` decorator to `edit_expense_view` — do not inline the session check

## Definition of done
- [ ] `GET /expenses/<id>/edit` renders a form pre-filled with the expense's current amount, category, date, and description
- [ ] `GET /expenses/<id>/edit` for an expense belonging to a different user returns 404
- [ ] `GET /expenses/<id>/edit` while logged out redirects to `/login`
- [ ] Submitting valid changes via POST updates the record in the database
- [ ] Updated values appear immediately on the dashboard after redirect
- [ ] Submitting with an invalid amount (e.g. `-10`, `0`, `abc`) re-renders the form with an error and does not update the DB
- [ ] Submitting with a future date re-renders the form with an error and does not update the DB
- [ ] Submitting with an out-of-whitelist category re-renders the form with an error and does not update the DB
- [ ] `created_at` for the edited expense is unchanged after a successful update
- [ ] Each row in the dashboard expense table has an Edit link pointing to the correct URL
- [ ] All new SQL in `db.py` uses `?` placeholders — no f-strings or string concatenation
