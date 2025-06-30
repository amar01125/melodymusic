#!/usr/bin/env python3
"""
Telegram Music Bot - Main Entry Point
A bot that searches and streams audio from YouTube with queue management
"""

import logging
import asyncio
import os
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.handlers import (
    start_handler, help_handler, search_handler, play_handler, download_handler,
    queue_handler, skip_handler, stop_handler, button_callback_handler,
    error_handler
)
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot"""
    # Get bot token from environment
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        return
    
    # Create application
    application = Application.builder().token(bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("search", search_handler))
    application.add_handler(CommandHandler("play", play_handler))
    application.add_handler(CommandHandler("download", download_handler))
    application.add_handler(CommandHandler("queue", queue_handler))
    application.add_handler(CommandHandler("skip", skip_handler))
    application.add_handler(CommandHandler("stop", stop_handler))
    
    # Add callback query handler for inline keyboards
    application.add_handler(CallbackQueryHandler(button_callback_handler))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Log startup
    logger.info("Starting Telegram Music Bot...")
    
    # Start the bot
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == '__main__':
    main()
