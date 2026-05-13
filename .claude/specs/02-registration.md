# Spec: Registration

## Overview
Step 2 introduces the full user-facing shell of Spendly: a landing page, a registration form, and a login form. Users can create an account with their name, email, and password, and log in to establish a session. This step transforms the bare health-check API into a real Flask web app with Jinja2 templates, a shared layout, and Flask session-based authentication — the foundation every subsequent feature depends on.

## Depends on
- Step 1 — Database Setup (`users` and `expenses` tables, `get_db()`, `init_db()`, `seed_db()`)

## Routes
- `GET /` — Render `landing.html` marketing/welcome page — public
- `GET /register` — Render `register.html` registration form — public
- `POST /register` — Validate form, insert user, redirect to `/login` on success — public
- `GET /login` — Render `login.html` login form — public
- `POST /login` — Validate credentials, set `session['user_id']`, redirect to `/` on success — public

## Database changes
No new tables or columns. Two new query helpers are needed in `database/db.py`:
- `get_user_by_email(email)` — returns a single Row or `None`
- `create_user(name, email, password_hash)` — inserts a new user row, returns the new `lastrowid`
 
## Templates
**Create:**
- `templates/base.html` — shared layout with `<head>`, nav bar, flash message block, `{% block content %}{% endblock %}`
- `templates/landing.html` — extends `base.html`; hero section with links to Register and Login
- `templates/register.html` — extends `base.html`; form with name, email, password, confirm-password fields
- `templates/login.html` — extends `base.html`; form with email and password fields

**Modify:**
- None

## Files to change
- `app.py` — replace health-check stub with real routes (`GET /`, `GET|POST /register`, `GET|POST /login`); add `app.secret_key`; import session, redirect, url_for, request, flash, render_template
- `database/db.py` — add `get_user_by_email()` and `create_user()`

## Files to create
- `templates/base.html`
- `templates/landing.html`
- `templates/register.html`
- `templates/login.html`
- `static/css/style.css` — global styles using CSS variables
- `static/css/landing.css` — landing-page-only overrides

## New dependencies
No new dependencies. `werkzeug.security` is already available via Flask.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — `?` placeholders, never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash()`; verified with `check_password_hash()`
- Use CSS variables — never hardcode hex values in stylesheets
- All templates must extend `base.html`
- `app.secret_key` must be set before any session usage; use a hard-coded dev key (`'dev-secret-key'`) for now — flag it as TODO for production
- Duplicate email on `POST /register` must return the form with a flash error, not a 500
- Wrong credentials on `POST /login` must return the form with a generic flash error (never reveal which field is wrong)
- All internal links in templates use `url_for()` — never hardcode paths
- DB helpers (`get_user_by_email`, `create_user`) live in `database/db.py`, not inline in route functions
- Flash messages must be displayed in `base.html` so every page inherits them
- After successful registration redirect to `/login`, not `/` — forces explicit login

## Definition of done
- [ ] `GET /` returns 200 and renders the landing page with links to `/register` and `/login`
- [ ] `GET /register` returns 200 and shows a form with name, email, password, confirm-password fields
- [ ] `POST /register` with valid unique data inserts a new user and redirects to `/login`
- [ ] `POST /register` with a duplicate email re-renders the form with a flash error message
- [ ] `POST /register` with mismatched passwords re-renders the form with a flash error message
- [ ] `GET /login` returns 200 and shows a form with email and password fields
- [ ] `POST /login` with valid credentials sets `session['user_id']` and redirects to `/`
- [ ] `POST /login` with wrong password re-renders the form with a generic flash error
- [ ] `POST /login` with unknown email re-renders the form with a generic flash error
- [ ] Passwords are stored as hashes (not plaintext) in the `users` table
- [ ] All template links use `url_for()` — verified by grep for hardcoded `/register`, `/login`, `/`
