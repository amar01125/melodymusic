# Telegram Music Bot

## Overview

This is a Telegram bot that allows users to search and stream audio from YouTube with queue management capabilities. The bot is built using Python with the `python-telegram-bot` library and `yt-dlp` for YouTube audio extraction. It provides a simple interface for users to search, play, queue, and manage music playback within Telegram chats.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Bot Layer**: Handles Telegram interactions and user commands
- **Service Layer**: Manages YouTube operations and queue management
- **Configuration Layer**: Centralizes all configuration settings
- **Utility Layer**: Provides common helper functions

The bot uses an event-driven architecture where Telegram commands trigger specific handlers that interact with various services to fulfill user requests.

## Key Components

### Bot Handlers (`bot/handlers.py`)
- **Purpose**: Processes Telegram commands and user interactions
- **Key Features**: Command routing, inline keyboard handling, error management
- **Commands Supported**: `/start`, `/help`, `/search`, `/play`, `/queue`, `/skip`, `/stop`

### YouTube Service (`bot/youtube_service.py`)
- **Purpose**: Handles YouTube search and audio extraction
- **Technology**: Uses `yt-dlp` library for YouTube operations
- **Features**: Asynchronous video search, audio extraction with quality control

### Queue Manager (`bot/queue_manager.py`)
- **Purpose**: Manages music playback queues per chat
- **Features**: Queue manipulation, current song tracking, skip functionality
- **Limits**: Maximum 50 songs per queue (configurable)

### Configuration (`config.py`)
- **Purpose**: Centralizes all bot settings and options
- **Key Settings**: Audio quality, rate limits, file paths, YouTube-DL options
- **Environment Variables**: Bot token, YouTube API key

### Utilities (`bot/utils.py`)
- **Purpose**: Common helper functions
- **Features**: Duration formatting, YouTube URL validation, video ID extraction

## Data Flow

1. **User Command**: User sends a command via Telegram
2. **Handler Processing**: Appropriate handler processes the command
3. **Service Interaction**: Handler calls relevant services (YouTube, Queue)
4. **Response Generation**: Handler formats and sends response back to user
5. **State Management**: Queue state is maintained per chat session

For audio playback:
1. User searches for music → YouTube Service searches and returns results
2. User selects track → Queue Manager adds to queue
3. Bot downloads audio → Temporary file created
4. Audio streamed to chat → File cleaned up after playback

## External Dependencies

### Required APIs
- **Telegram Bot API**: For bot communication (requires `TELEGRAM_BOT_TOKEN`)
- **YouTube API**: Optional, for enhanced search capabilities (requires `YOUTUBE_API_KEY`)

### Python Libraries
- `python-telegram-bot`: Telegram bot framework
- `yt-dlp`: YouTube audio extraction
- `asyncio`: Asynchronous operations

### System Requirements
- Python 3.7+
- Internet connection for YouTube access
- Temporary storage for audio files

## Deployment Strategy

### Environment Setup
- Set `TELEGRAM_BOT_TOKEN` environment variable
- Optionally set `YOUTUBE_API_KEY` for enhanced features
- Ensure adequate disk space for temporary audio files

### File Structure
- Temporary files stored in `./temp` directory
- Logs written to `bot.log`
- Configuration managed through environment variables

### Scaling Considerations
- Per-chat queue management allows concurrent usage
- Rate limiting prevents API abuse (10 requests/minute)
- Temporary file cleanup prevents storage issues

## Changelog

- June 30, 2025: Successfully deployed and fully tested bot functionality
  - Fixed package installation conflicts between telegram and python-telegram-bot
  - Resolved import errors by installing system packages
  - Fixed YouTube search with proper ytsearch: syntax in yt-dlp
  - Installed ffmpeg and fixed audio download functionality
  - Implemented dual command system: /play for voice chat streaming, /download for MP3 files
  - Fixed Markdown parsing errors in message formatting
  - Bot fully operational: search returns results, audio downloads and plays successfully
  - All core features tested and working: search, play, download, queue management
- June 29, 2025: Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.