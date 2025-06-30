#!/usr/bin/env python3
"""
Test YouTube search functionality
"""

import yt_dlp
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_youtube_search():
    """Test basic YouTube search"""
    search_opts = {
        'quiet': False,
        'no_warnings': False,
        'extract_flat': True
    }
    
    try:
        with yt_dlp.YoutubeDL(search_opts) as ytdl:
            print("Testing search for 'Never Gonna Give You Up'...")
            search_query = "ytsearch5:Never Gonna Give You Up"
            search_results = ytdl.extract_info(search_query, download=False)
            
            print(f"Search results type: {type(search_results)}")
            if search_results:
                print(f"Keys in results: {search_results.keys()}")
                if 'entries' in search_results:
                    print(f"Number of entries: {len(search_results['entries'])}")
                    for i, entry in enumerate(search_results['entries'][:3]):
                        if entry:
                            print(f"Entry {i}: {entry.get('title', 'No title')} - ID: {entry.get('id', 'No ID')}")
                        else:
                            print(f"Entry {i}: None")
                else:
                    print("No 'entries' key found")
            else:
                print("No search results returned")
                
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback
        traceback.print_exc()

def test_video_info():
    """Test getting video info"""
    info_opts = {
        'quiet': False,
        'no_warnings': False,
        'extract_flat': False
    }
    
    try:
        with yt_dlp.YoutubeDL(info_opts) as ytdl:
            print("\nTesting video info for Rick Roll...")
            info = ytdl.extract_info("dQw4w9WgXcQ", download=False)
            
            if info:
                print(f"Title: {info.get('title', 'No title')}")
                print(f"Duration: {info.get('duration', 'No duration')}")
                print(f"Uploader: {info.get('uploader', 'No uploader')}")
            else:
                print("No video info returned")
                
    except Exception as e:
        print(f"Error getting video info: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_youtube_search()
    test_video_info()