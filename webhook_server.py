# webhook_server.py
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.handlers import (
    start_command, help_command, download_command, search_command,
    lyrics_command, info_command, top_command, genre_command, handle_message
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-app.onrender.com

app = Flask(__name__)
application = ApplicationBuilder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start_command))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("download", download_command))
application.add_handler(CommandHandler("search", search_command))
application.add_handler(CommandHandler("lyrics", lyrics_command))
application.add_handler(CommandHandler("info", info_command))
application.add_handler(CommandHandler("top", top_command))
application.add_handler(CommandHandler("genre", genre_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

@app.route("/")
def root():
    return "Bot is alive and using webhook."

if __name__ == "__main__":
    import asyncio
    async def run():
        await application.initialize()
        await application.bot.set_webhook(WEBHOOK_URL + "/webhook")
        await application.start()
        await application.updater.start_polling()

    asyncio.get_event_loop().create_task(run())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
