#!/usr/bin/env python3
"""
Simple Telegram Music Bot
A minimal version to test functionality
"""

import os
import sys
import logging
import subprocess

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def install_dependencies():
    """Install required packages manually"""
    packages = [
        'python-telegram-bot==20.7',
        'yt-dlp'
    ]
    
    for package in packages:
        try:
            logger.info(f"Installing {package}...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                '--target', './.pythonlibs/lib/python3.11/site-packages',
                '--no-deps', package
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully installed {package}")
            else:
                logger.error(f"Failed to install {package}: {result.stderr}")
        except Exception as e:
            logger.error(f"Error installing {package}: {e}")

def main():
    """Main function"""
    # Check if bot token exists
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set!")
        print("❌ Bot token is missing. Please provide your Telegram Bot Token.")
        return
    
    # Install dependencies
    os.makedirs('.pythonlibs/lib/python3.11/site-packages', exist_ok=True)
    install_dependencies()
    
    # Add to Python path
    sys.path.insert(0, './.pythonlibs/lib/python3.11/site-packages')
    
    try:
        # Now try to import and run the bot
        from telegram.ext import Application, CommandHandler
        from telegram import Update
        from telegram.ext import ContextTypes
        
        logger.info("Successfully imported telegram libraries!")
        
        # Simple command handler
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text('🎵 Music Bot is working! Send /help for commands.')
        
        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            help_text = """
🎵 Music Bot Commands:
/start - Start the bot
/help - Show this help message
/search <query> - Search for music
/play <query> - Play music

Example: /search Never Gonna Give You Up
            """
            await update.message.reply_text(help_text)
        
        # Create application
        application = Application.builder().token(bot_token).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        
        logger.info("Starting Telegram Music Bot...")
        print("✅ Bot is starting up...")
        
        # Start the bot
        application.run_polling(allowed_updates=["message"])
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        print(f"❌ Failed to import telegram libraries: {e}")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        print(f"❌ Error starting bot: {e}")

if __name__ == '__main__':
    main()