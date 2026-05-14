# Spec: Delete Expense

## Overview
This step lets logged-in users permanently remove an expense they own. A single `POST /expenses/<id>/delete` route handles the deletion — no separate confirmation page is needed; the confirmation is a `window.confirm()` dialog triggered in the dashboard before the form submits. Ownership is verified server-side before any DELETE is executed so users cannot delete each other's records.

## Depends on
- Step 01 — database setup (`expenses` table, `get_db()`)
- Step 03 — login/logout (`login_required` decorator, session)
- Step 04 — user expense dashboard (the table from which delete is triggered)
- Step 05 — add expenses (expenses exist to delete)

## Routes
- `POST /expenses/<int:expense_id>/delete` — verify ownership, delete the row, redirect to `/dashboard` — logged-in only

## Database changes
No new tables or columns. One new helper function in `database/db.py`:

- `delete_expense(expense_id, user_id)` — deletes the row from `expenses` where `id = ?` AND `user_id = ?`. The double-condition WHERE clause is the ownership check; no rows are affected if the expense belongs to a different user. Uses parameterised `?` placeholders.

## Templates
- **Create:** none
- **Modify:** `templates/dashboard.html` — add a delete button/form per expense row. Each button submits a `<form method="POST">` targeting `url_for('delete_expense', expense_id=expense.id)`. A `window.confirm()` call in `static/js/main.js` (or inline `onclick`) prevents accidental submission.

## Files to change
- `app.py` — implement `POST /expenses/<int:expense_id>/delete` route (currently a stub).
- `database/db.py` — add `delete_expense(expense_id, user_id)` helper.
- `templates/dashboard.html` — add per-row delete form/button.
- `app.py` import line — add `delete_expense` to the import from `database.db`.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` via `get_db()` only
- Parameterised queries only — never f-strings in SQL
- `login_required` decorator must guard the route
- Ownership must be enforced in the SQL WHERE clause (`user_id = ?`), not in Python after fetching
- Route must only accept `POST` — `GET /expenses/<id>/delete` should return 405
- If the expense does not exist or belongs to another user, flash an error and redirect to `/dashboard` — do not raise a 404 (avoids leaking which IDs exist)
- On success: `flash('Expense deleted.', 'success')` then `redirect(url_for('dashboard'))`
- The delete trigger in the template must be a `<form method="POST">` — no JS `fetch`/XHR
- A `window.confirm()` dialog must fire before the form submits to prevent accidental deletion
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `url_for()` for every internal link — never hardcode URLs

## Definition of done
- [ ] Visiting `POST /expenses/<id>/delete` while logged out redirects to `/login`
- [ ] Clicking the delete button on the dashboard shows a `window.confirm()` dialog
- [ ] Cancelling the confirm dialog leaves the expense intact and the page unchanged
- [ ] Confirming the dialog submits the form, deletes the expense from the DB, flashes "Expense deleted.", and redirects to `/dashboard`
- [ ] The deleted expense no longer appears in the dashboard expense list
- [ ] The dashboard summary totals update to reflect the removed expense
- [ ] Attempting to delete an expense owned by a different user (e.g. via crafted POST) does not delete the row and redirects to `/dashboard` with an error flash
- [ ] Attempting to delete a non-existent expense ID redirects to `/dashboard` with an error flash
- [ ] Sending a `GET` request to `/expenses/<id>/delete` returns a 405 Method Not Allowed
