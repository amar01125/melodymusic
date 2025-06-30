#!/usr/bin/env python3
"""
Test bot search functionality
"""

import asyncio
from bot.youtube_service import YouTubeService

async def test_search():
    """Test the search functionality"""
    ys = YouTubeService()
    
    # Test search
    print("Testing search for 'Never Gonna Give You Up'...")
    results = await ys.search_videos('Never Gonna Give You Up', 3)
    
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result.get('title', 'No title')} - {result.get('duration', 0)}s")
    
    return len(results) > 0

if __name__ == '__main__':
    success = asyncio.run(test_search())
    print(f"Search test {'PASSED' if success else 'FAILED'}")