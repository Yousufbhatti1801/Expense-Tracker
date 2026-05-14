# Spec: PKR Currency Formatting

## Overview
Spendly currently formats all monetary values using the GBP symbol (£) via a Jinja2 `currency` filter hardcoded in `app.py`. This step switches the app's default currency to Pakistani Rupee (PKR), formatted as `Rs X,XXX.XX` (e.g. `Rs 1,500.00`). The change is applied globally through the existing filter — no new routes, DB columns, or templates are required. All places that render expense amounts automatically pick up the new format.

## Depends on
- Step 05 (Add Expenses) — the `add_expense` route and dashboard display that surface currency amounts must already exist.

## Routes
No new routes.

## Database changes
No database changes.

## Templates
- **Modify:** `templates/dashboard.html` — no template code changes needed; the Jinja2 `{{ amount | currency }}` calls already exist and will automatically reflect the updated filter.
- **Modify:** `templates/add_expense.html` — same as above; any amount placeholder or hint text showing the currency symbol should be updated to `Rs` where present as static text.

## Files to change
- `app.py` — update the `currency_filter` function (lines 11–13) to format amounts as `Rs {value:,.2f}` instead of `£{value:,.2f}`.
- `templates/add_expense.html` — replace any hardcoded `£` currency hints/placeholders with `Rs`.
- `templates/dashboard.html` — replace any hardcoded `£` currency hints/labels with `Rs`.

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs.
- Parameterised queries only (no change to DB in this step, but maintain the rule).
- Use CSS variables — never hardcode hex values.
- All templates extend `base.html`.
- The filter must remain registered as `currency` so every existing `| currency` call site continues to work without modification.
- Do **not** add a per-user currency preference column or settings page — this step is a global default change only.
- Search for every occurrence of `£` across all templates and Python files; replace each one with `Rs`.

## Definition of done
- [ ] The dashboard shows all expense amounts formatted as `Rs X,XXX.XX` (e.g. `Rs 1,500.00`).
- [ ] The per-category summary on the dashboard also shows amounts in `Rs`.
- [ ] The "Add Expense" form shows `Rs` wherever a currency symbol appeared as a hint or placeholder.
- [ ] No `£` symbol appears anywhere in the rendered UI.
- [ ] Existing tests (if any) referencing the currency symbol pass after updating expected strings.
- [ ] Running `grep -r "£" templates/ static/ app.py` returns no results.
