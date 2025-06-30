import os
from flask import Flask, request
from simple_bot import bot, dp
from aiogram import types
import asyncio

app = Flask(__name__)
loop = asyncio.get_event_loop()

WEBHOOK_PATH = f"/webhook/{bot.token}"
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL", "") + WEBHOOK_PATH

@app.route("/", methods=["GET"])
def index():
    return "Bot is running with webhook!"

@app.route(WEBHOOK_PATH, methods=["POST"])
def handle_webhook():
    try:
        update = types.Update(**request.json)
        loop.create_task(dp.process_update(update))
    except Exception as e:
        print(f"Webhook error: {e}")
    return "OK"

async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown():
    await bot.delete_webhook()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    loop.run_until_complete(on_startup())
    app.run(host="0.0.0.0", port=port)