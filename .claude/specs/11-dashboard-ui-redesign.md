# Spec: Dashboard UI Redesign

## Overview
Step 11 gives the dashboard a comprehensive visual overhaul to make Spendly feel like a polished product rather than a functional prototype. The charts and data pipeline are already solid (Step 08); this step focuses purely on aesthetics, layout hierarchy, and UX polish — improved summary cards with icons and trend indicators, a cleaner expense table, tighter mobile layout, and consistent micro-interactions (hover states, smooth transitions). No new data or routes are introduced; every change is CSS and template structure.

## Depends on
- Step 04 — dashboard route and expense data
- Step 06 — PKR currency formatting filter
- Step 08 — chart section, time-range API, Chart.js integration

## Routes
No new routes.

## Database changes
No database changes.

## Templates
- **Modify:** `templates/dashboard.html`
  - Restructure summary section: three-column cards with icon, label, value, and optional trend badge
  - Add a "Quick Stats" row: highest single expense, most-used category, number of expenses this month
  - Improve chart section layout: cards with header (title + time-range selector inline) and subtle border/shadow
  - Redesign expense table: sticky header, alternating row shading, category colour-dot badge, amount right-aligned and bold, action buttons as icon-only with tooltip
  - Add per-section empty-state illustrations (SVG inline or img) replacing bare text
  - Wrap page in a max-width container with consistent gutter padding

## Files to change
- `templates/dashboard.html` — structural and class changes as described above
- `static/css/dashboard.css` — full redesign of dashboard-scoped rules; use CSS variables throughout

## Files to create
None — all changes go into existing files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — all DB access stays in `database/db.py`
- Parameterised queries only — no f-strings in SQL
- Passwords hashed with werkzeug (unchanged by this step)
- Use CSS variables (`--color-*`, `--spacing-*`) — never hardcode hex values directly in rules
- All templates extend `base.html`
- No JS frameworks — vanilla JS only; Chart.js is already loaded
- Do not add new pip packages
- Do not change any route logic in `app.py` or any function in `database/db.py`
- Chart.js configuration lives in `static/js/main.js`; only touch it if chart visual options (colours, fonts) need updating — do not alter data-fetching logic
- Mobile-first CSS: start with a single-column layout, add grid/flex breakpoints for ≥768 px
- Icons must be inline SVG or a CDN icon font already referenced in `base.html` — do not add new CDN links unless `base.html` already includes them

## Definition of done
- [ ] Dashboard loads without JS errors in the browser console
- [ ] Summary cards display icon, label, formatted PKR value, and a trend badge (or "—" when no prior data)
- [ ] "Quick Stats" row shows highest single expense amount, most-used category name, and count of expenses this month — all sourced from existing Jinja variables, no new API calls
- [ ] Time-range selector sits inside the chart card header (not below the chart)
- [ ] Doughnut and bar charts still update correctly when a time-range button is clicked
- [ ] Expense table has sticky column headers, alternating row background, category colour-dot badge, right-aligned bold amount, and icon-only edit/delete buttons
- [ ] Empty state is shown (with a graphic and message) when the expense list is empty
- [ ] Page is usable on a 375 px viewport (no horizontal scroll, no overlapping elements)
- [ ] All colours reference CSS variables — `grep hardcoded-hex dashboard.css` returns no matches for raw hex values not assigned to a variable
- [ ] `pytest` passes with no regressions
