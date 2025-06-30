"""
Queue Manager
Manages music playback queue for each chat
"""

import logging
from typing import List, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

class QueueManager:
    """Manages music queue for a chat"""
    
    def __init__(self):
        """Initialize queue manager"""
        self.queue: List[Dict] = []
        self.current_index = 0
    
    def add_song(self, song_info: Dict) -> int:
        """Add a song to the queue
        
        Args:
            song_info: Dictionary containing song information
            
        Returns:
            Position in queue (0 means now playing)
        """
        if len(self.queue) >= Config.MAX_QUEUE_SIZE:
            raise Exception(f"Queue is full (max {Config.MAX_QUEUE_SIZE} songs)")
        
        self.queue.append(song_info)
        return len(self.queue) - 1
    
    def get_current_song(self) -> Optional[Dict]:
        """Get currently playing song"""
        if not self.queue or self.current_index >= len(self.queue):
            return None
        return self.queue[self.current_index]
    
    def skip_song(self) -> Optional[Dict]:
        """Skip current song and move to next
        
        Returns:
            Skipped song info or None if no song was playing
        """
        if not self.queue or self.current_index >= len(self.queue):
            return None
        
        skipped_song = self.queue[self.current_index]
        self.current_index += 1
        
        # Clean up finished songs
        if self.current_index > 0:
            self.queue = self.queue[self.current_index:]
            self.current_index = 0
        
        return skipped_song
    
    def get_queue(self) -> List[Dict]:
        """Get current queue starting from current song"""
        if not self.queue:
            return []
        
        return self.queue[self.current_index:]
    
    def clear_queue(self):
        """Clear the entire queue"""
        self.queue.clear()
        self.current_index = 0
    
    def remove_song(self, index: int) -> Optional[Dict]:
        """Remove a song from the queue by index
        
        Args:
            index: Index in the current queue (0 = currently playing)
            
        Returns:
            Removed song info or None if index is invalid
        """
        actual_index = self.current_index + index
        
        if actual_index < 0 or actual_index >= len(self.queue):
            return None
        
        removed_song = self.queue.pop(actual_index)
        
        # Adjust current index if needed
        if actual_index < self.current_index:
            self.current_index -= 1
        
        return removed_song
    
    def get_queue_info(self) -> Dict:
        """Get queue information"""
        current_queue = self.get_queue()
        
        return {
            'total_songs': len(current_queue),
            'current_song': self.get_current_song(),
            'queue_duration': sum(song.get('duration', 0) for song in current_queue),
            'is_empty': len(current_queue) == 0
        }
    
    def move_song(self, from_index: int, to_index: int) -> bool:
        """Move a song to a different position in the queue
        
        Args:
            from_index: Current position (0 = currently playing)
            to_index: New position
            
        Returns:
            True if successful, False otherwise
        """
        current_queue = self.get_queue()
        
        if (from_index < 0 or from_index >= len(current_queue) or 
            to_index < 0 or to_index >= len(current_queue) or
            from_index == to_index):
            return False
        
        # Don't allow moving the currently playing song
        if from_index == 0:
            return False
        
        actual_from = self.current_index + from_index
        actual_to = self.current_index + to_index
        
        # Move the song
        song = self.queue.pop(actual_from)
        self.queue.insert(actual_to, song)
        
        return True
    
    def shuffle_queue(self):
        """Shuffle the queue (excluding currently playing song)"""
        import random
        
        if len(self.queue) <= self.current_index + 1:
            return  # Nothing to shuffle
        
        # Shuffle only the upcoming songs
        upcoming_songs = self.queue[self.current_index + 1:]
        random.shuffle(upcoming_songs)
        
        # Reconstruct queue
        self.queue = (self.queue[:self.current_index + 1] + upcoming_songs)
