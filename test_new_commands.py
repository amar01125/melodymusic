#!/usr/bin/env python3
"""
Test the new /play and /download commands
"""

import asyncio
from bot.youtube_service import YouTubeService
from bot.utils import format_duration

async def test_commands():
    """Test both play and download functionality"""
    ys = YouTubeService()
    
    print("Testing YouTube search for 'levels'...")
    
    try:
        # Test search functionality
        results = await ys.search_videos("levels", max_results=1)
        
        if results:
            video_info = results[0]
            print(f"Found: {video_info['title']}")
            print(f"Duration: {format_duration(video_info['duration'])}")
            print(f"YouTube URL: https://youtube.com/watch?v={video_info['id']}")
            
            # Test audio download
            print("\nTesting audio download...")
            audio_path = await ys.download_audio(video_info['id'])
            
            if audio_path:
                print(f"Audio downloaded successfully: {audio_path}")
                return True
            else:
                print("Audio download failed")
                return False
        else:
            print("No search results found")
            return False
            
    except Exception as e:
        print(f"Test error: {e}")
        return False

if __name__ == '__main__':
    success = asyncio.run(test_commands())
    print(f"\nCommand test {'PASSED' if success else 'FAILED'}")