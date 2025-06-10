import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

async def test_send_message():
    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text="✅ Telegram bot test message")

asyncio.run(test_send_message())
