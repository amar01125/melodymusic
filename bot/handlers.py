"""
Telegram Bot Handlers
Contains all command and callback handlers for the music bot
"""

import logging
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from bot.youtube_service import YouTubeService
from bot.queue_manager import QueueManager
from bot.utils import format_duration, is_valid_youtube_url, sanitize_filename
from config import Config

logger = logging.getLogger(__name__)

# Initialize services
youtube_service = YouTubeService()
queue_managers = {}  # Store queue managers per chat

def get_queue_manager(chat_id):
    """Get or create queue manager for a chat"""
    if chat_id not in queue_managers:
        queue_managers[chat_id] = QueueManager()
    return queue_managers[chat_id]

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(
        Config.WELCOME_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        Config.HELP_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )

async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /search command"""
    if not context.args:
        await update.message.reply_text(
            "Please provide a search query.\nExample: /search Bohemian Rhapsody"
        )
        return
    
    query = ' '.join(context.args)
    
    # Send "searching" message
    searching_msg = await update.message.reply_text("🔍 Searching for music...")
    
    try:
        # Search for videos
        results = await youtube_service.search_videos(query, max_results=5)
        
        if not results:
            await searching_msg.edit_text("❌ No results found for your search.")
            return
        
        # Create inline keyboard with results
        keyboard = []
        for i, video in enumerate(results):
            duration = format_duration(video.get('duration', 0))
            button_text = f"🎵 {video['title'][:40]}... ({duration})"
            callback_data = f"play_{video['id']}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await searching_msg.edit_text(
            f"🎵 Search results for: *{query}*\n\nSelect a song to play:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error in search handler: {e}")
        await searching_msg.edit_text("❌ An error occurred while searching. Please try again.")

async def play_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /play command - for voice chat streaming"""
    if not context.args:
        await update.message.reply_text(
            "🎵 Voice Chat Streaming\n\n"
            "Please provide a song name or YouTube URL.\n"
            "Example: /play Never Gonna Give You Up\n\n"
            "Note: To download MP3 files, use /download instead."
        )
        return
    
    query = ' '.join(context.args)
    chat_id = update.effective_chat.id
    queue_manager = get_queue_manager(chat_id)
    
    # Send "processing" message
    processing_msg = await update.message.reply_text("🔍 Finding music for voice chat...")
    
    try:
        # Check if it's a YouTube URL or search query
        if is_valid_youtube_url(query):
            video_info = await youtube_service.get_video_info(query)
        else:
            # Search for the song
            results = await youtube_service.search_videos(query, max_results=1)
            if not results:
                await processing_msg.edit_text("❌ No results found for your search.")
                return
            video_info = results[0]
        
        # Check duration limit
        if video_info.get('duration', 0) > Config.MAX_DURATION:
            await processing_msg.edit_text(
                f"❌ Song is too long ({format_duration(video_info['duration'])}). "
                f"Maximum duration is {format_duration(Config.MAX_DURATION)}."
            )
            return
        
        # Add to queue
        position = queue_manager.add_song(video_info)
        
        # For voice chat, provide instructions and YouTube link
        title = video_info['title'].replace('*', '').replace('_', '').replace('[', '').replace(']', '').replace('`', '')
        safe_query = query.replace('*', '').replace('_', '').replace('[', '').replace(']', '').replace('`', '')
        
        message_text = (
            f"🎵 *Voice Chat Ready*\n\n"
            f"Song: {title}\n"
            f"Duration: {format_duration(video_info['duration'])}\n"
            f"Position in queue: {position + 1}\n\n"
            f"🔗 Stream URL: https://youtube.com/watch?v={video_info['id']}\n\n"
            f"📱 *To play in voice chat:*\n"
            f"1. Start a voice chat in this group\n"
            f"2. Use screen sharing to play the YouTube link\n"
            f"3. Or use a music bot that supports voice streaming\n\n"
            f"💾 Want to download instead? Use /download {safe_query}"
        )
        
        await processing_msg.edit_text(message_text, parse_mode=ParseMode.MARKDOWN)
            
    except Exception as e:
        logger.error(f"Error in play handler: {e}")
        await processing_msg.edit_text("❌ An error occurred while processing your request.")

async def download_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /download command - for MP3 file downloads"""
    if not context.args:
        await update.message.reply_text(
            "💾 Download MP3 Files\n\n"
            "Please provide a song name or YouTube URL.\n"
            "Example: /download Never Gonna Give You Up\n\n"
            "Note: For voice chat streaming, use /play instead."
        )
        return
    
    query = ' '.join(context.args)
    
    # Send "processing" message
    processing_msg = await update.message.reply_text("💾 Finding and downloading your music...")
    
    try:
        # Check if it's a YouTube URL or search query
        if is_valid_youtube_url(query):
            video_info = await youtube_service.get_video_info(query)
        else:
            # Search for the song
            results = await youtube_service.search_videos(query, max_results=1)
            if not results:
                await processing_msg.edit_text("❌ No results found for your search.")
                return
            video_info = results[0]
        
        # Check duration limit
        if video_info.get('duration', 0) > Config.MAX_DURATION:
            await processing_msg.edit_text(
                f"❌ Song is too long ({format_duration(video_info['duration'])}). "
                f"Maximum duration is {format_duration(Config.MAX_DURATION)}."
            )
            return
        
        # Download immediately without using queue
        title = video_info['title'].replace('*', '').replace('_', '').replace('[', '').replace(']', '').replace('`', '')
        
        message_text = (
            f"💾 Now downloading: {title}\n"
            f"Duration: {format_duration(video_info['duration'])}\n"
            f"Please wait..."
        )
        
        await processing_msg.edit_text(message_text, parse_mode=ParseMode.MARKDOWN)
        
        # Download and send audio file immediately - no queue involved
        await download_and_send_audio(update, context, video_info, processing_msg)
            
    except Exception as e:
        logger.error(f"Error in download handler: {e}")
        await processing_msg.edit_text("❌ An error occurred while processing your request.")

async def queue_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /queue command"""
    chat_id = update.effective_chat.id
    queue_manager = get_queue_manager(chat_id)
    
    queue_list = queue_manager.get_queue()
    
    if not queue_list:
        await update.message.reply_text("📝 Queue is empty.")
        return
    
    message = "📝 Current Queue:\n\n"
    for i, song in enumerate(queue_list):
        status = "🎵 Now Playing" if i == 0 else f"#{i}"
        message += f"{status} - {song['title']}\n"
        message += f"   Duration: {format_duration(song.get('duration', 0))}\n\n"
    
    await update.message.reply_text(message)

async def skip_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /skip command"""
    chat_id = update.effective_chat.id
    queue_manager = get_queue_manager(chat_id)
    
    current_song = queue_manager.get_current_song()
    if not current_song:
        await update.message.reply_text("❌ No song is currently playing.")
        return
    
    skipped_song = queue_manager.skip_song()
    next_song = queue_manager.get_current_song()
    
    if next_song:
        await update.message.reply_text(
            f"⏭️ Skipped: {skipped_song['title']}\n"
            f"🎵 Now playing: {next_song['title']}"
        )
        # Here you would typically start playing the next song
        # For this implementation, we'll just send the audio file
        processing_msg = await update.message.reply_text("🎵 Preparing next song...")
        await download_and_send_audio(update, context, next_song, processing_msg)
    else:
        await update.message.reply_text(f"⏭️ Skipped: {skipped_song['title']}\n📝 Queue is now empty.")

async def stop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stop command"""
    chat_id = update.effective_chat.id
    queue_manager = get_queue_manager(chat_id)
    
    current_song = queue_manager.get_current_song()
    if not current_song:
        await update.message.reply_text("❌ No song is currently playing.")
        return
    
    queue_manager.clear_queue()
    await update.message.reply_text("⏹️ Stopped playback and cleared queue.")

async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline keyboard button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith('play_'):
        video_id = query.data.replace('play_', '')
        chat_id = update.effective_chat.id
        queue_manager = get_queue_manager(chat_id)
        
        try:
            # Get video info
            video_info = await youtube_service.get_video_info(f"https://youtube.com/watch?v={video_id}")
            
            # Check duration limit
            if video_info.get('duration', 0) > Config.MAX_DURATION:
                await query.edit_message_text(
                    f"❌ Song is too long ({format_duration(video_info['duration'])}). "
                    f"Maximum duration is {format_duration(Config.MAX_DURATION)}."
                )
                return
            
            # Add to queue
            position = queue_manager.add_song(video_info)
            
            if position == 0:
                await query.edit_message_text(
                    f"🎵 Now playing: *{video_info['title']}*\n"
                    f"Duration: {format_duration(video_info['duration'])}\n"
                    f"Downloading and sending...",
                    parse_mode=ParseMode.MARKDOWN
                )
                
                # Download and send audio
                await download_and_send_audio(update, context, video_info, query.message)
            else:
                await query.edit_message_text(
                    f"✅ Added to queue (position {position + 1}): *{video_info['title']}*\n"
                    f"Duration: {format_duration(video_info['duration'])}",
                    parse_mode=ParseMode.MARKDOWN
                )
                
        except Exception as e:
            logger.error(f"Error in button callback: {e}")
            await query.edit_message_text("❌ An error occurred while processing your selection.")

async def download_and_send_audio(update: Update, context: ContextTypes.DEFAULT_TYPE, video_info: dict, message):
    """Download and send audio file to user"""
    try:
        # Download audio
        audio_path = await youtube_service.download_audio(video_info['id'])
        
        if not audio_path or not os.path.exists(audio_path):
            await message.edit_text("❌ Failed to download audio.")
            return
        
        # Update message
        title = video_info['title'].replace('*', '').replace('_', '').replace('[', '').replace(']', '').replace('`', '')
        await message.edit_text(
            f"📤 Sending: {title}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Send audio file
        with open(audio_path, 'rb') as audio_file:
            await context.bot.send_audio(
                chat_id=update.effective_chat.id,
                audio=audio_file,
                title=video_info['title'],
                duration=video_info.get('duration', 0),
                caption=f"🎵 {video_info['title']}\n🔗 https://youtube.com/watch?v={video_info['id']}"
            )
        
        # Clean up
        try:
            os.remove(audio_path)
        except:
            pass
            
        # Update final message
        await message.edit_text(
            f"✅ Sent: {title}",
            parse_mode=ParseMode.MARKDOWN
        )
        
    except Exception as e:
        logger.error(f"Error downloading/sending audio: {e}")
        await message.edit_text("❌ Failed to download or send audio.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle bot errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An unexpected error occurred. Please try again later."
        )
