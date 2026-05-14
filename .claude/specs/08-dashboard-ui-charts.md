# Spec: Dashboard UI Charts

## Overview
Step 08 adds visual, filterable charts to the existing dashboard, transforming the
text-only category breakdown into an interactive spending summary.

Users will be able to view their expenses across different time ranges:

- Yesterday
- Last 7 days / weekly
- Last 1 month
- Last 6 months

The dashboard will include a time-range filter control. When the user selects a
different filter, the charts must update accordingly without requiring a full page
reload.

The category chart should show spending distribution for the selected period, and
the time-based chart should show spending trends for that same selected period.

A doughnut chart will show spending by category, and a bar chart will show spending
over time based on the selected filter.

Examples:

- `6months` filter shows monthly totals for the last 6 calendar months
- `1month` filter shows daily totals for the last 1 month
- `weekly` filter shows daily totals for the last 7 days
- `yesterday` filter shows expenses for yesterday only

Charts will be rendered client-side using Chart.js loaded from a CDN — no npm and
no pip packages. A JSON endpoint will provide filtered chart data for the logged-in
user.

No new dashboard page is needed. The existing `GET /dashboard` route remains the
main page, while `/api/expenses/summary` returns chart data based on the selected
time range.

All chart data must be scoped to the logged-in user using `session['user_id']`.
The charts must update when the user changes the selected filter, and the dashboard
must handle empty results gracefully by showing a “No data yet” message instead of
empty charts.

## Depends on
- Step 01 — Database setup (`expenses` table)
- Step 04 — Dashboard display (`dashboard.html`, `dashboard.css`, summary data flow)
- Step 05 — Add expenses
- Step 07 — Delete expense

## Routes
No new dashboard route.

Add one JSON API endpoint:

- `GET /api/expenses/summary?range=6months|1month|weekly|yesterday`

This endpoint returns filtered chart data as JSON and must be logged-in only.

Example response:

```json
{
  "selected_range": "6months",
  "by_category": [
    {
      "category": "Food",
      "total": 2500.0
    },
    {
      "category": "Transport",
      "total": 1200.0
    }
  ],
  "by_period": [
    {
      "label": "2025-12",
      "total": 0
    },
    {
      "label": "2026-01",
      "total": 1500.0
    }
  ]
}
```

## Database changes
No new tables or columns.

Add new helper functions to `database/db.py`:

```python
def get_category_summary_by_range(user_id, range_filter):
    """
    Returns category-wise spending totals for the selected time range.
    """
```

```python
def get_period_summary_by_range(user_id, range_filter):
    """
    Returns time-based spending totals for the selected time range.
    """
```

Supported `range_filter` values:

- `yesterday`
- `weekly`
- `1month`
- `6months`

Behavior:

### Yesterday
- Category chart: category totals for yesterday only
- Bar chart: yesterday’s total grouped by date
- Missing data should return `0` instead of breaking the chart

### Weekly
- Category chart: category totals for the last 7 days
- Bar chart: daily totals for the last 7 days
- Missing days must show total `0`

### 1 Month
- Category chart: category totals for the last 1 month
- Bar chart: daily totals for the last 1 month
- Missing days must show total `0`

### 6 Months
- Category chart: category totals for the last 6 months
- Bar chart: monthly totals for the last 6 calendar months
- Missing months must show total `0`

All database queries must:

- Use `user_id` to scope data to the logged-in user
- Use parameterized SQL queries only
- Never expose another user’s data
- Return totals as numbers, not formatted currency strings
- Avoid SQL f-strings

## Templates
Modify:

- `templates/dashboard.html`

Add a charts section between the summary cards and the expense table.

The charts section should include:

- A time-range filter control
- A category chart card
- A spending trend chart card

Required HTML structure:

```html
<section class="dashboard-charts">
  <div class="charts-header">
    <h2>Spending Insights</h2>

    <select id="chart-range-filter">
      <option value="6months">Last 6 months</option>
      <option value="1month">Last 1 month</option>
      <option value="weekly">Last 7 days</option>
      <option value="yesterday">Yesterday</option>
    </select>
  </div>

  <div class="charts-grid">
    <div class="chart-card">
      <h3>Spending by Category</h3>
      <canvas id="category-chart"></canvas>
      <p class="chart-empty-state" id="category-empty-state">No data yet</p>
    </div>

    <div class="chart-card">
      <h3>Spending Over Time</h3>
      <canvas id="period-chart"></canvas>
      <p class="chart-empty-state" id="period-empty-state">No data yet</p>
    </div>
  </div>
</section>
```

Load Chart.js from CDN near the bottom of the dashboard template:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
```

Add JavaScript that:

- Fetches `/api/expenses/summary?range=6months` on initial page load
- Fetches new data when the user changes the filter
- Updates both charts without a full page reload
- Shows empty-state messages when there is no data
- Destroys old Chart.js instances before creating new ones
- Uses CSS variable values for chart colors

## Files to change
- `app.py`
  - Add `GET /api/expenses/summary` route
  - Protect it with `@login_required`
  - Read the selected range from `request.args.get("range")`
  - Validate range values
  - Return JSON using `jsonify()`

- `database/db.py`
  - Add `get_category_summary_by_range(user_id, range_filter)`
  - Add `get_period_summary_by_range(user_id, range_filter)`

- `templates/dashboard.html`
  - Add charts section
  - Add time-range filter dropdown
  - Add Chart.js CDN script
  - Add JavaScript to fetch and render chart data

- `static/css/dashboard.css`
  - Add chart layout styles
  - Add `.dashboard-charts`
  - Add `.charts-header`
  - Add `.charts-grid`
  - Add `.chart-card`
  - Add `.chart-empty-state`
  - Add responsive chart styles

## Files to create
None.

## New dependencies
No new Python dependencies.

Frontend dependency allowed:

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
```

No npm packages.
No local Chart.js copy.
No pip packages.

## API behavior
The API endpoint must support:

```txt
GET /api/expenses/summary?range=6months
GET /api/expenses/summary?range=1month
GET /api/expenses/summary?range=weekly
GET /api/expenses/summary?range=yesterday
```

If no range is provided, default to:

```txt
6months
```

If an invalid range is provided, default to:

```txt
6months
```

The API must return:

```json
{
  "selected_range": "6months",
  "by_category": [],
  "by_period": []
}
```

The API must not return another user’s data.

## Chart behavior
The dashboard must include two charts.

### 1. Category-wise spending chart
Chart type:

```txt
doughnut
```

Data source:

```txt
by_category
```

This chart shows how much the user spent in each category for the selected time range.

Example labels:

```txt
Food, Transport, Bills, Shopping, Other
```

Example values:

```txt
2500, 1200, 5000, 3000, 900
```

### 2. Time-based spending chart
Chart type:

```txt
bar
```

Data source:

```txt
by_period
```

This chart shows spending over time for the selected range.

Behavior:

- `6months` shows monthly bars
- `1month` shows daily bars
- `weekly` shows daily bars
- `yesterday` shows one daily bar

Missing periods must appear with value `0`.

## Frontend rules
- Do not hardcode chart data in JavaScript
- Fetch chart data from `/api/expenses/summary`
- Use the selected filter value in the API query string
- Use Chart.js for rendering charts
- Store chart instances in variables so they can be destroyed before re-rendering
- Prevent duplicate charts from stacking on top of each other
- Check that canvas elements exist before rendering charts
- Use `getComputedStyle(document.documentElement)` to read CSS variables
- Do not use hardcoded hex colors in JavaScript
- Show “No data yet” if the selected range has no expenses
- Hide or visually disable the chart canvas when there is no data
- No JavaScript errors should appear in the browser console

## Styling rules
- Use CSS variables only
- Never hardcode hex colors
- No inline `style=""` attributes
- Charts must be responsive
- Chart cards should match the existing dashboard design
- Use spacing, borders, rounded corners, and subtle shadows
- The filter dropdown should be styled consistently with the rest of the app
- On mobile screens, chart cards should stack vertically

## Rules for implementation
- No SQLAlchemy or ORMs
- Use raw SQLite with `get_db()`
- Use parameterized queries only
- Never use f-strings inside SQL queries
- Password/auth logic must not be changed
- All templates must extend `base.html`
- The dashboard route must remain protected by `@login_required`
- The API route must be protected by `@login_required`
- Use `session['user_id']` for all chart queries
- Never expose another user’s expense data
- Do not remove existing summary cards
- Do not remove existing expense table
- Do not remove Add Expense button
- Do not remove Delete buttons/links
- Do not implement new add/edit/delete logic in this step
- Keep existing dashboard functionality working
- Keep currency formatting consistent with the rest of the app

## Empty state behavior
If the user has no expenses for the selected range:

- Show “No data yet” in the category chart card
- Show “No data yet” in the period chart card
- Do not render empty broken charts
- Do not show JavaScript errors
- Keep the time-range filter visible
- Keep the existing dashboard and expense table visible

## Definition of done
- [ ] Dashboard includes a time-range filter
- [ ] Filter options include Yesterday, Last 7 days, Last 1 month, and Last 6 months
- [ ] `/api/expenses/summary` accepts a `range` query parameter
- [ ] `/api/expenses/summary` returns `selected_range`, `by_category`, and `by_period`
- [ ] `/api/expenses/summary` is protected by `@login_required`
- [ ] Invalid or missing range defaults to `6months`
- [ ] Category chart updates when the filter changes
- [ ] Time-based bar chart updates when the filter changes
- [ ] Charts update without a full page reload
- [ ] Category chart shows correct totals for the selected range
- [ ] Bar chart shows correct totals for the selected range
- [ ] Weekly filter shows the last 7 days
- [ ] One-month filter shows daily totals for the last 1 month
- [ ] Six-month filter shows monthly totals for the last 6 months
- [ ] Yesterday filter shows yesterday’s spending only
- [ ] Missing days/months show `0`
- [ ] User with no expenses sees “No data yet”
- [ ] Charts are responsive
- [ ] Chart colors use CSS variables
- [ ] No hardcoded chart data exists in JavaScript
- [ ] No hardcoded hex colors exist in dashboard chart CSS or JS
- [ ] Existing summary cards remain unchanged
- [ ] Existing expense table remains unchanged
- [ ] Add Expense button remains visible
- [ ] Delete buttons/links remain visible
- [ ] No add/edit/delete CRUD logic is implemented in this step
- [ ] No other user’s expense data is visible
- [ ] No JavaScript errors appear in the browser console