# Spec: Railway Deploy

## Overview
Step 12 makes Spendly deployable to Railway, a Platform-as-a-Service that builds and runs the app from the GitHub repo. Gunicorn is already in `requirements.txt`; this step wires up the remaining production config: a `Procfile` so Railway knows how to start the app, a `railway.toml` that pins the build settings, and a small fix in `app.py` so the server binds to the `$PORT` env var Railway injects at runtime (instead of the hardcoded 5001). A `SECRET_KEY` env var must be set in the Railway dashboard — the spec documents this as a manual step. SQLite is used as-is; Railway's filesystem is ephemeral so data does not persist across redeploys, which is acceptable for this personal-tracker scope.

## Depends on
- Step 01 — database schema and `init_db()` / `seed_db()` helpers must exist
- All prior steps (the app must be fully functional before shipping)

## Routes
No new routes.

## Database changes
No database changes.

**Note:** Railway runs on an ephemeral filesystem. The SQLite file at `spendly.db` is recreated (and re-seeded) on every fresh deploy. This is a known limitation acceptable at this stage. The `DATABASE_URL` env var in `db.py` already supports overriding the path if a persistent volume is mounted later.

## Templates
- **Create:** None
- **Modify:** None

## Files to change
- `app.py` — bind to `$PORT` env var at runtime; disable `debug` in production

## Files to create
- `Procfile` — tells Railway (and Heroku-compatible hosts) how to start the app with Gunicorn
- `railway.toml` — pins build command, start command, and healthcheck path

## New dependencies
No new dependencies. (`gunicorn` is already in `requirements.txt`.)

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — no f-strings in SQL
- Passwords hashed with werkzeug (unchanged by this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Do not change any route logic or DB functions
- `SECRET_KEY` must never be hardcoded — read exclusively from the env var; the existing fallback string is only for local dev and must not be used in production
- `debug=True` must not run in production — gate it on `FLASK_ENV != 'production'`
- Port must be read from `os.environ.get('PORT', 5001)` so Railway's dynamic port injection works
- Gunicorn must bind to `0.0.0.0:$PORT` — not localhost

## Definition of done
- [ ] `Procfile` exists at the repo root with a valid `web:` line using Gunicorn
- [ ] `railway.toml` exists at the repo root and specifies the start command and healthcheck
- [ ] `app.py` reads `PORT` from the environment — `os.environ.get('PORT', 5001)` — and passes it to `app.run()`
- [ ] `app.py` only sets `debug=True` when `FLASK_ENV` is not `production`
- [ ] Running `gunicorn "app:app" --bind 0.0.0.0:5001` locally starts the app without errors
- [ ] The landing page loads at `http://localhost:5001` when started via Gunicorn
- [ ] `pytest` passes with no regressions after the changes
- [ ] After pushing to Railway (via `/railway-deploy`), the Railway dashboard shows a green deployment
- [ ] The live Railway URL loads the Spendly landing page
- [ ] `SECRET_KEY` is set as an env var in the Railway dashboard (manual step — documented in this spec)
