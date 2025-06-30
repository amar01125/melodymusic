#!/usr/bin/env python3
"""
Test audio download functionality
"""

import asyncio
import os
from bot.youtube_service import YouTubeService

async def test_download():
    """Test audio download"""
    ys = YouTubeService()
    
    print("Testing audio download for Rick Roll...")
    # Test with a known working video ID
    video_id = "dQw4w9WgXcQ"  # Rick Roll
    
    try:
        audio_path = await ys.download_audio(video_id)
        
        if audio_path and os.path.exists(audio_path):
            file_size = os.path.getsize(audio_path)
            print(f"Download successful: {audio_path}")
            print(f"File size: {file_size} bytes")
            
            # Clean up
            os.remove(audio_path)
            return True
        else:
            print("Download failed - no file created")
            return False
            
    except Exception as e:
        print(f"Download error: {e}")
        return False

if __name__ == '__main__':
    success = asyncio.run(test_download())
    print(f"Download test {'PASSED' if success else 'FAILED'}")