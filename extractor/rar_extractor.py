# ============================================================================
# RAR EXTRACTOR - Extract .rar compressed files
# ============================================================================

from .base_extractor import BaseExtractor
from typing import Dict, Any, List
import logging
import rarfile
import tempfile
from pathlib import Path

class RARExtractor(BaseExtractor):
    """Extract content from RAR archive files"""
    
    def extract(self) -> Dict[str, Any]:
        """
        Extract RAR archive files
        
        Returns:
            Dictionary with extracted content
        """
        try:
            with rarfile.RarFile(self.file_path, 'r') as rar:
                # Get file list
                file_list = rar.namelist()
                
                extracted_files = []
                
                # Extract to temp directory
                with tempfile.TemporaryDirectory() as temp_dir:
                    rar.extractall(path=temp_dir)
                    
                    # Read extracted files
                    for filename in file_list:
                        file_path = Path(temp_dir) / filename
                        
                        if file_path.is_file():
                            try:
                                # Try to read as text
                                try:
                                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                                        content = f.read()
                                    
                                    extracted_files.append({
                                        'filename': filename,
                                        'size': file_path.stat().st_size,
                                        'type': 'text',
                                        'content': content
                                    })
                                except:
                                    # Binary file
                                    extracted_files.append({
                                        'filename': filename,
                                        'size': file_path.stat().st_size,
                                        'type': 'binary',
                                        'note': 'Binary content'
                                    })
                            except Exception as e:
                                self.logger.warning(f"Could not read {filename}: {e}")
                
                content = {
                    'type': 'rar_archive',
                    'total_files': len(file_list),
                    'extracted_files': len(extracted_files),
                    'files': extracted_files
                }
                
                return self.create_result_dict(content)
                
        except Exception as e:
            self.logger.error(f"RAR extraction error: {e}")
            return self.create_result_dict(
                content={'error': str(e)},
                status='error',
                error_message=str(e)
            )
