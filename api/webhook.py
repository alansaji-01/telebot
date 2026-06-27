import os
import json
from http.server import BaseHTTPRequestHandler

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]

AUTO_REPLIES = {
    "hello": "Hey! Alan is currently unavailable. 👋",
    "hi": "Hey! Alan is currently unavailable. 👋",
    "urgent": "🚨 Alan will be notified."
}

DEFAULT_REPLY = (
    "Hi! I'm Alan's auto-reply bot.\n"
    "Alan is currently busy and will reply soon."
)

application = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm Alan's assistant bot.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send any message and I'll auto-reply.")


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


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length)

        update = Update.de_json(json.loads(body), application.bot)

        import asyncio
        asyncio.run(application.initialize())
        asyncio.run(application.process_update(update))

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Telegram Bot Running")