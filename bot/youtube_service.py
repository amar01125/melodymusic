"""
YouTube Service
Handles YouTube search and audio extraction using yt-dlp
"""

import logging
import asyncio
import yt_dlp
import os
from typing import List, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

class YouTubeService:
    """Service for YouTube operations"""
    
    def __init__(self):
        """Initialize YouTube service"""
        self.ytdl_opts = Config.YTDL_OPTIONS.copy()
        self.ytdl = yt_dlp.YoutubeDL(self.ytdl_opts)
        
        # Ensure temp directory exists
        os.makedirs(Config.TEMP_DIR, exist_ok=True)
    
    async def search_videos(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search for videos on YouTube"""
        try:
            # Run in executor to avoid blocking
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None, 
                self._search_videos_sync, 
                query, 
                max_results
            )
            return results
        except Exception as e:
            logger.error(f"Error searching videos: {e}")
            return []
    
    def _search_videos_sync(self, query: str, max_results: int) -> List[Dict]:
        """Synchronous video search"""
        search_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True
        }
        
        try:
            with yt_dlp.YoutubeDL(search_opts) as ytdl:
                # Use proper YouTube search format
                search_query = f"ytsearch{max_results}:{query}"
                search_results = ytdl.extract_info(search_query, download=False)
                
                if not search_results or 'entries' not in search_results:
                    logger.error(f"No search results for query: {query}")
                    return []
                
                videos = []
                for entry in search_results['entries']:
                    if entry and entry.get('id'):
                        # Get additional info for each video
                        video_info = self._get_video_info_sync(entry['id'])
                        if video_info:
                            videos.append(video_info)
                
                logger.info(f"Found {len(videos)} videos for query: {query}")
                return videos
                
        except Exception as e:
            logger.error(f"Error in sync search: {e}")
            return []
    
    async def get_video_info(self, url: str) -> Optional[Dict]:
        """Get information about a YouTube video"""
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._get_video_info_sync, 
                url
            )
            return result
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return None
    
    def _get_video_info_sync(self, url_or_id: str) -> Optional[Dict]:
        """Synchronous video info extraction"""
        try:
            # Handle both URLs and video IDs
            if not url_or_id.startswith('http'):
                url_or_id = f"https://youtube.com/watch?v={url_or_id}"
            
            info_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False
            }
            
            with yt_dlp.YoutubeDL(info_opts) as ytdl:
                info = ytdl.extract_info(url_or_id, download=False)
                
                if not info:
                    return None
                
                return {
                    'id': info.get('id', ''),
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'url': info.get('webpage_url', ''),
                    'thumbnail': info.get('thumbnail', '')
                }
                
        except Exception as e:
            logger.error(f"Error getting video info sync: {e}")
            return None
    
    async def download_audio(self, video_id: str) -> Optional[str]:
        """Download audio from YouTube video"""
        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._download_audio_sync, 
                video_id
            )
            return result
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            return None
    
    def _download_audio_sync(self, video_id: str) -> Optional[str]:
        """Synchronous audio download"""
        try:
            url = f"https://youtube.com/watch?v={video_id}"
            
            # Configure download options - download best audio directly
            download_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'outtmpl': os.path.join(Config.TEMP_DIR, f'{video_id}.%(ext)s'),
                'restrictfilenames': True,
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(download_opts) as ytdl:
                ytdl.download([url])
                
                # Find the downloaded file (any audio format)
                for file in os.listdir(Config.TEMP_DIR):
                    if video_id in file and any(file.endswith(ext) for ext in ['.m4a', '.webm', '.mp3', '.aac']):
                        file_path = os.path.join(Config.TEMP_DIR, file)
                        logger.info(f"Downloaded audio: {file_path}")
                        return file_path
                
                logger.error(f"No audio file found for video ID: {video_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error in sync download: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            for file in os.listdir(Config.TEMP_DIR):
                file_path = os.path.join(Config.TEMP_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")
