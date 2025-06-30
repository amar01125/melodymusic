#!/usr/bin/env python3
"""
Test that download works without queue
"""

import asyncio
from bot.youtube_service import YouTubeService

async def test_multiple_downloads():
    """Test multiple downloads work independently"""
    ys = YouTubeService()
    
    test_queries = ["test", "hello", "music"]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: Searching for '{query}'")
        results = await ys.search_videos(query, max_results=1)
        
        if results:
            video_info = results[0]
            print(f"  Found: {video_info['title']}")
            
            # Test download
            audio_path = await ys.download_audio(video_info['id'])
            if audio_path:
                import os
                if os.path.exists(audio_path):
                    size = os.path.getsize(audio_path)
                    print(f"  Download SUCCESS: {size} bytes")
                    os.remove(audio_path)
                else:
                    print(f"  Download FAILED: file not found")
            else:
                print(f"  Download FAILED: no path returned")
        else:
            print(f"  No results found")
        
        print()

if __name__ == '__main__':
    asyncio.run(test_multiple_downloads())