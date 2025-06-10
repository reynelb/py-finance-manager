# notifier.py
This file implements the `PaymentNotifier` class for Telegram notifications.

## Responsibilities
- Load environment variables (Telegram bot token).
- Send formatted Telegram messages to notify about payments.
- Periodically check for upcoming payments and notify users.

## Key Components
- `PaymentNotifier` class:
  - Checks if any payment is due in the next 3 days.
  - Sends reminder messages using the Telegram Bot API.
- Uses `asyncio` and `python-telegram-bot`.
