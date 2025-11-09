# ============================================================================
# TAR EXTRACTOR - Extract .tar compressed files
# ============================================================================

from .base_extractor import BaseExtractor
from typing import Dict, Any, List
import logging
import tarfile
import tempfile
from pathlib import Path

class TARExtractor(BaseExtractor):
    """Extract content from TAR archive files"""
    
    def extract(self) -> Dict[str, Any]:
        """
        Extract TAR archive files
        
        Returns:
            Dictionary with extracted content
        """
        try:
            with tarfile.open(self.file_path, 'r') as tar:
                members = tar.getmembers()
                
                extracted_files = []
                for member in members:
                    if member.isfile():
                        try:
                            # Extract file content
                            file_obj = tar.extractfile(member)
                            if file_obj:
                                file_content = file_obj.read()
                                
                                # Try to decode as text
                                try:
                                    text_content = file_content.decode('utf-8', errors='replace')
                                    extracted_files.append({
                                        'filename': member.name,
                                        'size': member.size,
                                        'type': 'text',
                                        'content': text_content
                                    })
                                except:
                                    extracted_files.append({
                                        'filename': member.name,
                                        'size': member.size,
                                        'type': 'binary',
                                        'note': 'Binary content'
                                    })
                        except Exception as e:
                            self.logger.warning(f"Could not extract {member.name}: {e}")
                
                content = {
                    'type': 'tar_archive',
                    'total_files': len(members),
                    'extracted_files': len(extracted_files),
                    'files': extracted_files
                }
                
                return self.create_result_dict(content)
                
        except Exception as e:
            self.logger.error(f"TAR extraction error: {e}")
            return self.create_result_dict(
                content={'error': str(e)},
                status='error',
                error_message=str(e)
            )
