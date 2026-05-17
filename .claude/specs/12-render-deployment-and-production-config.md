# Spec: Render Deployment and Production Config

## Overview
This step prepares Spendly for deployment on Render's free tier. It covers switching from
the hard-coded dev secret key to an environment-variable-driven config, making the SQLite
database path portable across both local and Render's persistent disk, adding a
`gunicorn`-based WSGI entry point, and providing the `render.yaml` service manifest so
the app can be deployed with a single click. No new user-facing features are introduced;
this step is purely infrastructure and production-hardening.

## Depends on
All previous steps (01–11) should be complete. The app must run correctly locally before
deployment is attempted.

## Routes
No new routes.

## Database changes
No database changes to the schema. The SQLite file path in `database/db.py` will be made
configurable via the `DATABASE_URL` environment variable so Render's persistent disk path
(`/var/data/spendly.db`) can be injected at runtime without touching source code.

## Templates
- **Modify:** None required.
  - `base.html` — optionally add an environment badge (dev vs production) if `FLASK_ENV`
    is set, but only if explicitly requested. Not required for definition of done.

## Files to change
- `app.py` — load `SECRET_KEY` from `os.environ` with a safe fallback only in dev;
  remove the inline `# TODO` comment; guard `seed_db()` call behind a dev-only flag so
  the demo user is not seeded in production.
- `database/db.py` — read `DB_PATH` from `DATABASE_URL` env var when present, else fall
  back to the current relative path (keeps local dev working with zero config).

## Files to create
- `wsgi.py` — minimal Gunicorn entry point:
  ```python
  from app import app  # noqa: F401
  ```
- `render.yaml` — Render service manifest defining the web service, build command,
  start command, environment variables (with `generateValue: true` for `SECRET_KEY`),
  and the persistent disk mount at `/var/data`.
- `requirements.txt` update — add `gunicorn` if not already present (check first).

## New dependencies
- `gunicorn` — production WSGI server required by Render. Add to `requirements.txt`.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only — no changes to existing SQL.
- Passwords hashed with werkzeug — no changes to auth logic.
- Use CSS variables — never hardcode hex values (no template changes needed here).
- All templates extend `base.html` — no new templates.
- `SECRET_KEY` must **never** have a hard-coded production value in source code; it must
  come from the environment.
- `DATABASE_URL` override must be optional — local dev must work without setting it.
- `seed_db()` must only run when `FLASK_ENV` is not `production` (or equivalent guard)
  to avoid overwriting real user data on first deploy.
- Do not install packages beyond `gunicorn` — no other additions to `requirements.txt`.
- The app still runs on port 5001 locally; Render injects its own `PORT` env var for
  the hosted instance — `wsgi.py` / `render.yaml` must handle this correctly.
- Keep `if __name__ == '__main__'` block in `app.py` for local `python app.py` usage.

## Definition of done
- [ ] `python app.py` still starts the dev server on port 5001 with no errors.
- [ ] `gunicorn wsgi:app` starts successfully locally (returns HTTP 200 on `/`).
- [ ] Deleting `spendly.db` and setting `DATABASE_URL=/tmp/test.db` then running the app
      creates the database at `/tmp/test.db`, not the default path.
- [ ] Starting the app with `FLASK_ENV=production` does **not** seed the demo user.
- [ ] Starting the app without `FLASK_ENV=production` seeds the demo user as before.
- [ ] `SECRET_KEY` is loaded from the environment; starting without it logs a warning or
      uses a clearly dev-only fallback (never a production secret in code).
- [ ] `render.yaml` is valid YAML and references `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
      as the start command.
- [ ] `requirements.txt` includes `gunicorn`.
- [ ] All existing pytest tests still pass after the changes.
