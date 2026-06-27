import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]

application = Application.builder().token(BOT_TOKEN).build()

AUTO_REPLIES = {
    "hello": "👋 Alan is currently busy.",
    "hi": "👋 Alan is currently busy.",
    "urgent": "🚨 Alan will be notified."
}

DEFAULT_REPLY = (
    "Hi!\n"
    "I'm Alan's assistant bot.\n"
    "Alan is currently unavailable and will reply soon."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm Alan's Telegram Assistant."
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
application.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply)
)


async def handler(request):
    await application.initialize()

    if request.method == "POST":
        body = await request.json()
        update = Update.de_json(body, application.bot)
        await application.process_update(update)

    return {
        "statusCode": 200,
        "body": "OK"
    }