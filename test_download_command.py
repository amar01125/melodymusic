#!/usr/bin/env python3
"""
Test download command functionality
"""

import asyncio
import os
from bot.youtube_service import YouTubeService
from bot.handlers import download_and_send_audio

async def test_download_flow():
    """Test the download flow"""
    ys = YouTubeService()
    
    print("Testing download flow...")
    
    # Test search
    results = await ys.search_videos("test", max_results=1)
    if not results:
        print("No search results")
        return False
    
    video_info = results[0]
    print(f"Found: {video_info['title']}")
    
    # Test audio download
    audio_path = await ys.download_audio(video_info['id'])
    if audio_path and os.path.exists(audio_path):
        file_size = os.path.getsize(audio_path)
        print(f"Download successful: {file_size} bytes")
        
        # Cleanup
        os.remove(audio_path)
        return True
    else:
        print("Download failed")
        return False

if __name__ == '__main__':
    success = asyncio.run(test_download_flow())
    print(f"Download flow test: {'PASSED' if success else 'FAILED'}")