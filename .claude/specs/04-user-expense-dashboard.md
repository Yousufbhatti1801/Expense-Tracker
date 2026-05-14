# Spec: User Expense Dashboard

## Overview
Step 4 introduces the core of Spendly: the authenticated dashboard at `/dashboard`
where users see a summary of their spending and a full list of their expenses.
This is the first logged-in page in the app, making it the natural destination
after login and the hub from which expense CRUD operations (Steps 5–7) will launch.
It replaces the current post-login redirect to the public landing page with a
meaningful, user-specific view.

## Depends on
- Step 01 — Database setup (`expenses` table, `get_db()`, `init_db()`, `seed_db()`)
- Step 02 — Registration (`users` table, `create_user`, `get_user_by_email`)
- Step 03 — Login / Logout (`login_required` decorator, `session['user_id']`)

## Routes
- `GET /dashboard` — render the user's expense dashboard — logged-in only

## Database changes
No new tables or columns. Two new query helpers are needed in `database/db.py`:
- `get_expenses_by_user(user_id)` — returns all expenses for the user ordered by `date DESC`
- `get_expense_summary(user_id)` — returns total spend and per-category totals for the user

## Templates
**Create:**
- `templates/dashboard.html` — extends `base.html`; shows summary cards and expense table

**Modify:**
- `templates/login.html` — change the success redirect target from `/` to `/dashboard`
  (update the route in `app.py`, not the template itself)
- `templates/base.html` — update the post-login nav link (if any) to point to `/dashboard`

## Files to change
- `app.py` — add `GET /dashboard` route protected by `login_required`; change post-login
  redirect from `url_for('landing')` to `url_for('dashboard')`
- `database/db.py` — add `get_expenses_by_user()` and `get_expense_summary()`

## Files to create
- `templates/dashboard.html`
- `static/css/dashboard.css` — dashboard-specific styles (summary cards, table)

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — `?` placeholders, never f-strings in SQL
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- The `/dashboard` route must be decorated with `login_required`
- Use `session['user_id']` to scope all queries — never expose another user's data
- `get_expenses_by_user` and `get_expense_summary` must live in `database/db.py`,
  not inline in the route function
- The expense table must show: date, category, description, amount
- Summary section must show at minimum: total spend and a per-category breakdown
- Format currency amounts consistently (e.g. `£12.50`) — use a Jinja2 filter or
  template formatting, not hardcoded symbols in Python
- The dashboard must render correctly with zero expenses (empty state message required)

## Dashboard actions
The dashboard should include visible action links/buttons for future expense CRUD features:
- **Add Expense** button/link — points to the future add expense route
- **Delete Expense** button/link for each expense row — points to the future delete expense route

These controls are only placeholders/navigation hooks in this step. The actual add and delete functionality will be implemented in later steps.

## Definition of done
- [ ] `GET /dashboard` returns 200 for a logged-in user
- [ ] `GET /dashboard` redirects to `/login` for an unauthenticated visitor
- [ ] Dashboard displays the logged-in user's name
- [ ] Dashboard shows correct total spend across all expenses
- [ ] Dashboard shows a per-category spending breakdown
- [ ] Dashboard shows a table of all expenses (date, category, description, amount)
- [ ] Expenses are ordered by date descending (most recent first)
- [ ] Dashboard renders without errors when the user has zero expenses (empty state shown)
- [ ] Successful login now redirects to `/dashboard` instead of `/`
- [ ] No other user's expenses are visible (queries are scoped by `session['user_id']`)
- [ ] All template links use `url_for()` — no hardcoded paths
