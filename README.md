# Expense Tracker (Boilerplate)

Starter scaffold for an expense tracker web app.
This is intentionally minimal and does **not** include deep business logic yet.

## Suggested Stack

- Frontend: Vanilla JS starter (can be swapped to React/Vue later)
- Backend: Node.js + Express starter API
- Shared: Reusable constants/contracts

## Folder Structure

```text
expense-tracker/
|-- frontend/
|   |-- index.html
|   |-- styles.css
|   `-- src/
|       |-- main.js
|       |-- components/
|       |-- pages/
|       `-- services/
|-- backend/
|   |-- package.json
|   |-- .env.example
|   `-- src/
|       |-- server.js
|       |-- app.js
|       |-- config/
|       |-- routes/
|       |-- controllers/
|       `-- middleware/
|-- shared/
|   `-- constants/
`-- docs/
```

## Quick Start

```bash
cd backend
npm install
npm run dev
```

Then open `frontend/index.html` in your browser (or serve it with any static server).

## Next Steps

- Add expense categories and transaction model
- Connect frontend form to backend API
- Add persistence (SQLite/PostgreSQL/MongoDB)
- Add authentication and dashboard charts
# Expense-Tracker
