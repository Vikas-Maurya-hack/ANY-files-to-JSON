# ============================================================================
# FILE SCANNER - Recursive directory scanning
# ============================================================================

from pathlib import Path
from typing import List, Set
from config import Config
import logging

class FileScanner:
    """Scan directories and collect supported files"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_extensions = self._get_all_extensions()
    
    def _get_all_extensions(self) -> Set[str]:
        """Get all supported file extensions"""
        extensions = set()
        for category in Config.SUPPORTED_EXTENSIONS.values():
            extensions.update(category)
        return extensions
    
    def scan_directory(self, directory: Path, recursive: bool = True) -> List[Path]:
        """
        Scan directory for supported files
        
        Args:
            directory: Directory to scan
            recursive: Scan subdirectories
            
        Returns:
            List of file paths
        """
        files = []
        
        try:
            if recursive:
                # Recursive scan - use rglob with wildcard
                for file_path in directory.rglob('*'):
                    if file_path.is_file():
                        if self._is_supported(file_path):
                            files.append(file_path)
                            self.logger.debug(f"Found: {file_path.name}")
            else:
                # Only immediate directory
                for file_path in directory.glob('*'):
                    if file_path.is_file():
                        if self._is_supported(file_path):
                            files.append(file_path)
                            self.logger.debug(f"Found: {file_path.name}")
            
            self.logger.info(f"Found {len(files)} supported files in {directory}")
        
        except PermissionError as e:
            self.logger.warning(f"Permission denied: {directory}")
        except Exception as e:
            self.logger.error(f"Error scanning {directory}: {e}")
        
        return files
    
    def _is_supported(self, file_path: Path) -> bool:
        """Check if file type is supported"""
        file_path_lower = str(file_path).lower()
        
        # Check for multi-part extensions first (.tar.gz, .tar.bz2, etc.)
        if file_path_lower.endswith(('.tar.gz', '.tar.bz2')):
            self.logger.debug(f"Supported (multi-ext): {file_path.name}")
            return True
        
        # Check standard extension
        ext = file_path.suffix.lower()
        is_supported = ext in self.supported_extensions
        
        if is_supported:
            self.logger.debug(f"Supported ({ext}): {file_path.name}")
        else:
            self.logger.debug(f"Unsupported ({ext}): {file_path.name}")
        
        return is_supported
    
    def get_file_stats(self, files: List[Path]) -> dict:
        """Get statistics about scanned files"""
        stats = {
            'total_files': len(files),
            'by_type': {},
            'total_size': 0
        }
        
        for file_path in files:
            # Count by extension
            ext = file_path.suffix.lower()
            stats['by_type'][ext] = stats['by_type'].get(ext, 0) + 1
            
            # Add size
            try:
                stats['total_size'] += file_path.stat().st_size
            except:
                pass
        
        # Convert size to human readable
        stats['total_size_human'] = self._human_readable_size(stats['total_size'])
        
        return stats
    
    def _human_readable_size(self, size_bytes: int) -> str:
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
