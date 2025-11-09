# ============================================================================
# PROGRESS TRACKER - Thread-safe progress tracking
# ============================================================================

import threading
from typing import Optional
from datetime import datetime, timedelta

class ProgressTracker:
    """Thread-safe progress tracker for multi-threaded extraction"""
    
    def __init__(self, total_files: int):
        self.total_files = total_files
        self.processed_files = 0
        self.successful = 0
        self.failed = 0
        self.skipped = 0
        self.start_time = datetime.now()
        self.lock = threading.Lock()
        self.current_file = ""
    
    def update(self, success: bool = True, skipped: bool = False, filename: str = ""):
        """Update progress counters"""
        with self.lock:
            self.processed_files += 1
            if skipped:
                self.skipped += 1
            elif success:
                self.successful += 1
            else:
                self.failed += 1
            self.current_file = filename
    
    def get_stats(self) -> dict:
        """Get current statistics"""
        with self.lock:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            
            # Calculate progress percentage
            progress = (self.processed_files / self.total_files * 100) if self.total_files > 0 else 0
            
            # Calculate speed (files per second)
            speed = self.processed_files / elapsed if elapsed > 0 else 0
            
            # Estimate time remaining
            if speed > 0:
                remaining_files = self.total_files - self.processed_files
                eta_seconds = remaining_files / speed
                eta = str(timedelta(seconds=int(eta_seconds)))
            else:
                eta = "Calculating..."
            
            return {
                'total': self.total_files,
                'processed': self.processed_files,
                'successful': self.successful,
                'failed': self.failed,
                'skipped': self.skipped,
                'progress_percent': round(progress, 2),
                'elapsed_time': str(timedelta(seconds=int(elapsed))),
                'speed': round(speed, 2),
                'eta': eta,
                'current_file': self.current_file
            }
    
    def get_progress_bar(self, width: int = 50) -> str:
        """Get text-based progress bar"""
        stats = self.get_stats()
        progress = stats['progress_percent'] / 100
        filled = int(width * progress)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}] {stats['progress_percent']:.1f}%"
