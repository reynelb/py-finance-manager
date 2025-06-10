# app/notifier.py
import os
from datetime import datetime
from app.manager import FinanceManager
from telegram import Bot
from dotenv import load_dotenv
import asyncio

load_dotenv()

class PaymentNotifier:
    def __init__(self, manager: FinanceManager):
        self.manager = manager
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.bot = Bot(token=self.token)

    def check_payments(self):
        today = datetime.now().date()
        upcoming = []
        for payment in self.manager.get_upcoming_payments():
            try:
                due_date = datetime.fromisoformat(payment.date).date()
                days_until = (due_date - today).days
                if 0 <= days_until <= 3:
                    upcoming.append((payment.description, due_date))
            except Exception:
                continue

        if upcoming:
            msg = "🔔 *Upcoming Payments*\n"
            for desc, date in upcoming:
                msg += f"• {desc} – Due: {date.strftime('%Y-%m-%d')}\n"
            self.send_reminder(msg)

    

    def send_reminder(self, message, chat_id):
        async def _send():
            await self.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        try:
            print("📤 Sending Telegram message...")
            asyncio.run(_send())
            print("✅ Message sent successfully.")
        except Exception as e:
            print("❌ Failed to send Telegram message:", e)




    
