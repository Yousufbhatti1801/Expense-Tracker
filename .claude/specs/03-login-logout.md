# Spec: Login and Logout

## Overview
This step completes the authentication layer by implementing the `/logout` route,
adding a `login_required` decorator to guard protected routes, and making the
navigation in `base.html` session-aware. Login (GET + POST) is already fully
implemented from Step 02; the outstanding work is logout, nav state, and auth
guards so the rest of the app can safely assume a logged-in user.

## Depends on
- Step 01 — Database setup (users table, get_db)
- Step 02 — Registration (create_user, get_user_by_email, login GET/POST)

## Routes
- `GET /logout` — clears session, redirects to `/` — public (but only meaningful when logged in)

## Database changes
No database changes.

## Templates
- **Modify:** `templates/base.html` — replace static nav links with session-aware
  conditional: show Register + Sign in when no session, show a greeting + Logout
  when `session.user_id` is set.

## Files to change
- `app.py` — add `/logout` route; add `login_required` decorator; apply decorator
  to any existing stub routes that require authentication (`/profile`, and any
  expense stubs that already exist as stubs)
- `templates/base.html` — session-aware nav

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (already in place — do not change)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `login_required` must be a proper decorator using `functools.wraps` so Flask
  can still resolve endpoint names correctly
- Logout must call `session.clear()`, not just `session.pop('user_id')`
- After logout redirect to `url_for('landing')`, not a hardcoded path
- Do not display the user's name in the nav by querying the DB on every request —
  use `session['user_name']` stored at login time instead
- The nav conditional must use `session.get('user_id')` (not `session['user_id']`)
  to avoid a KeyError when no session exists

## Definition of done
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/`
- [ ] Visiting `/logout` while already logged out also redirects to `/` without error
- [ ] After logout the nav shows Register + Sign in (not Logout)
- [ ] After login the nav shows the user's name and a Logout link (not Register/Sign in)
- [ ] Any route decorated with `login_required` redirects to `/login` when accessed without a session
- [ ] The `login_required` decorator preserves the original function name (Flask endpoint resolution works)
- [ ] A fresh registration → login → logout → login cycle completes without errors
