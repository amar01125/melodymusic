"""
Configuration settings for the Telegram Music Bot
"""

import os

class Config:
    """Configuration class for bot settings"""
    
    # Bot settings
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
    
    # Audio settings
    AUDIO_QUALITY = 'bestaudio/best'
    MAX_DURATION = 600  # 10 minutes in seconds
    AUDIO_FORMAT = 'mp3'
    
    # Queue settings
    MAX_QUEUE_SIZE = 50
    MAX_CONCURRENT_DOWNLOADS = 3
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 10
    
    # File paths
    TEMP_DIR = './temp'
    LOG_FILE = 'bot.log'
    
    # YouTube DL options
    YTDL_OPTIONS = {
        'format': AUDIO_QUALITY,
        'noplaylist': True,
        'extractaudio': True,
        'audioformat': AUDIO_FORMAT,
        'outtmpl': f'{TEMP_DIR}/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'logtostderr': False,
        'ignoreerrors': False,
        'no_warnings': True,
        'default_search': 'ytsearch',
        'source_address': '0.0.0.0'
    }
    
    # Messages
    WELCOME_MESSAGE = """
🎵 Welcome to Music Bot! 🎵

I can help you search and stream music from YouTube.

Available commands:
/start - Start the bot
/help - Show this help message
/search <query> - Search for music
/play <query> - Voice chat streaming
/download <query> - Download MP3 files
/queue - Show current queue
/skip - Skip current song
/stop - Stop playback and clear queue

Just send me a song name or YouTube URL and I'll find it for you!
    """
    
    HELP_MESSAGE = """
🎵 Music Bot Help 🎵

Commands:
• /search <query> - Search for songs on YouTube
• /play <query> - Voice chat streaming (provides YouTube link)
• /download <query> - Download and send MP3 files
• /queue - View current queue
• /skip - Skip current song
• /stop - Stop playback and clear queue

Examples:
• /search Bohemian Rhapsody
• /play Never Gonna Give You Up
• /download Shape of You
• Send me a YouTube URL directly

Features:
✅ Voice chat streaming support
✅ High-quality MP3 downloads
✅ Queue management
✅ Works in groups and private chats
✅ Supports YouTube URLs and search queries

Note: Songs are limited to 10 minutes duration.
    """
