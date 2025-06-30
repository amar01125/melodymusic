#!/usr/bin/env python3
"""
Simple test to check telegram bot installation
"""

try:
    from telegram.ext import Application
    print("✓ python-telegram-bot imported successfully")
    
    import yt_dlp
    print("✓ yt-dlp imported successfully")
    
    import os
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if bot_token:
        print("✓ TELEGRAM_BOT_TOKEN is available")
        
        # Test basic application creation
        app = Application.builder().token(bot_token).build()
        print("✓ Telegram Application created successfully")
        print("All dependencies are working correctly!")
    else:
        print("❌ TELEGRAM_BOT_TOKEN not found")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")