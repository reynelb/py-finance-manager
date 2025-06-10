# main.py
This script runs the command-line interface (CLI) version of the finance manager.

## Responsibilities
- Provides a terminal-based user menu to:
  - Add income or expense
  - View financial reports
  - Check upcoming payments manually or automatically
- Schedules periodic checks for payments using APScheduler.
- Runs an infinite loop that waits for user input.

## Key Components
- `FinanceManager`: Handles finance data.
- `PaymentNotifier`: Sends Telegram messages.
- `APScheduler`: Runs periodic payment checks (every 24h).
