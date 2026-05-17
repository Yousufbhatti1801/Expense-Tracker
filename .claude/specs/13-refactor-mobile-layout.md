# Spec: Refactor Mobile Layout

## Overview
This step audits and hardens the responsive layout across all Spendly pages so the app is fully usable on small screens (375px–480px) with no horizontal scroll, no clipped content, and consistent touch-friendly spacing. It consolidates the scattered mobile rules in `style.css`, `login.css`, and `dashboard.css` into a coherent, mobile-first system and fills the gaps left by earlier feature steps — particularly the nav, forms, and expense table — so every page works well on a phone before a tablet or desktop breakpoint kicks in.

## Depends on
- Step 01 — Database setup
- Step 02 — Registration
- Step 03 — Login and Logout
- Step 04 — User Expense Dashboard
- Step 05 — Add Expenses
- Step 07 — Delete Expense
- Step 08 — Dashboard UI Charts
- Step 10 — Expense Persistence Fix
- Step 11 — Dashboard UI Redesign

## Routes
No new routes.

## Database changes
No database changes.

## Templates
- **Modify:** `templates/base.html`
  - Add hamburger menu button (hidden on ≥768px, visible on mobile)
  - Add `id="nav-links"` to the nav links container for JS toggle
  - Ensure nav collapses to a vertical stack on small screens
- **Modify:** `templates/dashboard.html`
  - Wrap the expense table in a `<div class="table-scroll-wrapper">` for horizontal scroll containment on very narrow screens
  - Ensure action buttons (Edit/Delete) remain reachable on 375px
- **Modify:** `templates/add_expense.html`
  - Verify all form elements are full-width and touch-target sized (min 44px height)
- **Modify:** `templates/edit_expense.html`
  - Same as add_expense.html

## Files to change
- `static/css/style.css` — add mobile-first nav collapse rules, hamburger styles, and global touch-target sizing
- `static/css/dashboard.css` — tighten existing breakpoints, add table scroll wrapper rule, fix action button layout on mobile
- `static/css/login.css` — verify existing 480px rule still covers register page (both share the same card class)
- `static/css/landing.css` — add breakpoint for hero text and CTA button on 375px
- `static/js/main.js` — add hamburger toggle logic (toggle `nav-open` class on nav)
- `templates/base.html` — hamburger button markup
- `templates/dashboard.html` — table scroll wrapper
- `templates/add_expense.html` — touch-target audit
- `templates/edit_expense.html` — touch-target audit

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Mobile-first: base styles target 375px; use `min-width` breakpoints only (never `max-width` except where already established)
- Hamburger toggle must be pure vanilla JS — no libraries
- Touch targets must be ≥ 44px tall for all interactive elements on mobile
- No new pip packages
- Do not alter existing breakpoints in `dashboard.css` — only add rules on top of them
- The nav hamburger must hide gracefully on ≥768px without a JS check (CSS `display` swap is sufficient)

## Definition of done
- [ ] At 375px viewport width, the nav collapses and a hamburger icon appears; tapping it reveals the nav links in a vertical stack
- [ ] At 375px, no page produces horizontal scroll (check landing, login, register, dashboard, add expense, edit expense)
- [ ] At 375px, the dashboard expense table is scrollable horizontally within its container without causing full-page scroll
- [ ] At 375px, all form inputs and buttons are at least 44px tall and fill the available width
- [ ] At 375px, the landing page hero text and CTA button are readable and not clipped
- [ ] At ≥768px, the hamburger icon is hidden and the nav links are displayed inline as before
- [ ] All new CSS uses only existing CSS variables — no hardcoded hex values anywhere in the changed files
- [ ] `pytest` passes with no regressions
