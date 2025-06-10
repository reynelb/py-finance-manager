# app.py
This is the main Flask web application file for the Personal Finance Manager.

## Responsibilities
- Configure Flask and Flask-Login.
- Define routes for:
  - Home (`/`)
  - Register/Login/Logout
  - Dashboard display of financial data
  - Adding income, expenses, budgets, and payments
  - Linking a Telegram Chat ID to receive reminders
- Render templates and manage database sessions.

## Key Components
- `FinanceManager`: Backend logic for handling income/expenses.
- `PaymentNotifier`: Sends reminders about upcoming payments via Telegram.
- Uses SQLAlchemy for ORM and SQLite as the database backend.
