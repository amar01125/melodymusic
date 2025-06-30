"""
Utility functions for the Telegram Music Bot
"""

import re
import os
import logging
from typing import Optional
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)

def format_duration(seconds: int) -> str:
    """Format duration in seconds to MM:SS format"""
    if seconds <= 0:
        return "0:00"
    
    minutes = seconds // 60
    seconds = seconds % 60
    
    if minutes >= 60:
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    
    return f"{minutes}:{seconds:02d}"

def is_valid_youtube_url(url: str) -> bool:
    """Check if URL is a valid YouTube URL"""
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    
    return bool(youtube_regex.match(url))

def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from YouTube URL"""
    if not is_valid_youtube_url(url):
        return None
    
    # Handle different YouTube URL formats
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:v\/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for file system"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    
    return filename

def format_file_size(size_bytes: int) -> str:
    """Format file size in bytes to human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    size_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and size_index < len(size_names) - 1:
        size /= 1024
        size_index += 1
    
    return f"{size:.1f} {size_names[size_index]}"

def validate_search_query(query: str) -> bool:
    """Validate search query"""
    if not query or not query.strip():
        return False
    
    # Check length
    if len(query) > 100:
        return False
    
    # Check for valid characters
    if not re.match(r'^[a-zA-Z0-9\s\-_.,!?()]+$', query):
        return False
    
    return True

def get_file_extension(mime_type: str) -> str:
    """Get file extension from MIME type"""
    mime_map = {
        'audio/mpeg': 'mp3',
        'audio/mp4': 'm4a',
        'audio/ogg': 'ogg',
        'audio/wav': 'wav',
        'audio/flac': 'flac'
    }
    
    return mime_map.get(mime_type, 'mp3')

def clean_temp_directory(temp_dir: str, max_age_hours: int = 24):
    """Clean old files from temp directory"""
    try:
        import time
        
        if not os.path.exists(temp_dir):
            return
        
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                
                if file_age > max_age_seconds:
                    try:
                        os.remove(file_path)
                        logger.info(f"Removed old temp file: {filename}")
                    except Exception as e:
                        logger.error(f"Error removing temp file {filename}: {e}")
                        
    except Exception as e:
        logger.error(f"Error cleaning temp directory: {e}")

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."

def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

def is_admin(user_id: int, chat_id: int, bot) -> bool:
    """Check if user is admin in the chat"""
    try:
        chat_member = bot.get_chat_member(chat_id, user_id)
        return chat_member.status in ['creator', 'administrator']
    except Exception:
        return False

def rate_limit_key(user_id: int, chat_id: int) -> str:
    """Generate rate limit key for user"""
    return f"rate_limit_{user_id}_{chat_id}"

def log_user_action(user_id: int, username: str, action: str, details: str = ""):
    """Log user actions for monitoring"""
    logger.info(
        f"User action - ID: {user_id}, Username: {username}, "
        f"Action: {action}, Details: {details}"
    )
