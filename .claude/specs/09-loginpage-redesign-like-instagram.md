# Spec: Login Page Redesign (Instagram-style)

## Overview
Redesign the existing `/login` page with a clean, Instagram-inspired aesthetic:
a centred card with the Spendly logo/wordmark at the top, borderless inputs with
placeholder text, a full-width primary CTA button, an "OR" divider, and a
sign-up footer link. The route logic and session handling remain unchanged —
this step is purely a frontend (template + CSS) change. The goal is a polished,
app-like first impression that fits the existing design-token system.

## Depends on
- Step 03 — Login & Logout (route + session handling must be complete)
- Step 02 — Registration (register route must exist for the sign-up link)

## Routes
No new routes. `GET /login` and `POST /login` are unchanged.

## Database changes
No database changes.

## Templates
- **Modify:** `templates/login.html`
  - Remove the generic `.card` wrapper
  - Add a `.login-logo` section (Spendly wordmark + tagline)
  - Replace labelled inputs with borderless inputs using `placeholder=` text
  - Add a password visibility toggle button (eye icon, vanilla JS)
  - Add a full-width `.btn-login` submit button
  - Add an `.login-divider` ("OR" rule)
  - Add a `.login-signup-prompt` footer ("Don't have an account? **Sign up**")
  - Keep all flash messages (error/success) rendered above the form
  - All internal links use `url_for()`

## Files to change
- `templates/login.html` — full redesign (structure + class names)

## Files to create
- `static/css/login.css` — login-page-only styles (do not pollute `style.css`)

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only (no SQL changes in this step)
- Passwords hashed with werkzeug (no changes to auth logic)
- Use CSS variables — never hardcode hex values; extend with new variables if needed
- All templates extend `base.html`
- Load `login.css` via a `{% block extra_css %}` block in `login.html` only — do not add it to `base.html`
- Password toggle must be pure vanilla JS inline in the template `{% block scripts %}` block — no new `.js` file
- The redesign must be fully responsive down to 375 px wide (mobile-first)
- Flash messages must remain visible and correctly styled — do not remove or hide them
- Form `action` and `method` attributes must remain `{{ url_for('login') }}` and `POST`
- Input `name` attributes (`email`, `password`) must not change — the route reads them by name
- No inline `<style>` tags — all styles go in `login.css`

## Definition of done
- [ ] Navigating to `/login` shows the new Instagram-style layout: logo at top, borderless inputs, full-width button, OR divider, sign-up footer link
- [ ] Submitting correct credentials redirects to `/dashboard`
- [ ] Submitting wrong credentials shows the flash error message above the form
- [ ] Clicking the eye icon on the password field toggles visibility between `type="password"` and `type="text"`
- [ ] "Sign up" link in the footer navigates to `/register`
- [ ] Page looks correct on a 375 px wide viewport (no horizontal scroll, inputs full-width)
- [ ] No inline `<style>` tags exist in `login.html`
- [ ] All internal links use `url_for()` — no hardcoded paths
- [ ] `style.css` and `base.html` are unmodified
- [ ] Existing pages (landing, register, dashboard) are visually unaffected
