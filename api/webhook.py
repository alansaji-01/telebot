import os
import json
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

AUTO_REPLIES = {
    "hello": "👋 Hey! Alan is currently unavailable.",
    "hi": "👋 Hey! Alan is currently unavailable.",
    "urgent": "🚨 Alan has been notified.",
}

DEFAULT_REPLY = (
    "Hi! I'm Alan's assistant bot.\n"
    "Alan is currently busy and will reply as soon as possible."
)

application = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm Alan's assistant bot."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me a message and I'll reply automatically."
    )


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    reply = DEFAULT_REPLY

    for key, value in AUTO_REPLIES.items():
        if key in text:
            reply = value
            break

    await update.message.reply_text(reply)


application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply)
)


async def process(body):
    await application.initialize()

    update = Update.de_json(json.loads(body), application.bot)

    await application.process_update(update)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain"
        },
        "body": "OK"
    }


def handler(request):
    body = request.get_data(as_text=True)
    return asyncio.run(process(body))