# ============================================================================
# GZIP EXTRACTOR - Extract .gz, .tar.gz, .tgz compressed files
# ============================================================================

from .base_extractor import BaseExtractor
from typing import Dict, Any, List
import logging
import gzip
import tarfile
import tempfile
import os
from pathlib import Path

class GZIPExtractor(BaseExtractor):
    """Extract content from GZIP and TAR.GZ files"""
    
    def extract(self) -> Dict[str, Any]:
        """
        Extract GZIP compressed files
        
        Returns:
            Dictionary with extracted content
        """
        try:
            file_path_lower = str(self.file_path).lower()
            
            # Check if it's a tar.gz/tgz file
            if file_path_lower.endswith(('.tar.gz', '.tgz')):
                return self._extract_tar_gz()
            else:
                return self._extract_gzip()
                
        except Exception as e:
            self.logger.error(f"GZIP extraction failed: {e}")
            return self.create_result_dict(
                content={'error': str(e)},
                status='error',
                error_message=str(e)
            )
    
    def _extract_gzip(self) -> Dict[str, Any]:
        """Extract single .gz file"""
        try:
            with gzip.open(self.file_path, 'rb') as gz_file:
                # Read decompressed content
                decompressed_data = gz_file.read()
                
                # Try to decode as text
                try:
                    text_content = decompressed_data.decode('utf-8', errors='replace')
                    content = {
                        'type': 'gzip_text',
                        'text': text_content,
                        'size_compressed': self.file_path.stat().st_size,
                        'size_decompressed': len(decompressed_data),
                        'compression_ratio': f"{self.file_path.stat().st_size / len(decompressed_data):.2%}"
                    }
                except:
                    # Binary content
                    content = {
                        'type': 'gzip_binary',
                        'note': 'Binary content - not text',
                        'size_compressed': self.file_path.stat().st_size,
                        'size_decompressed': len(decompressed_data),
                        'compression_ratio': f"{self.file_path.stat().st_size / len(decompressed_data):.2%}"
                    }
            
            return self.create_result_dict(content)
            
        except Exception as e:
            self.logger.error(f"GZIP extraction error: {e}")
            return self.create_result_dict(
                content={'error': str(e)},
                status='error',
                error_message=str(e)
            )
    
    def _extract_tar_gz(self) -> Dict[str, Any]:
        """Extract tar.gz archive"""
        try:
            with tarfile.open(self.file_path, 'r:gz') as tar:
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
                    'type': 'tar_gz_archive',
                    'total_files': len(members),
                    'extracted_files': len(extracted_files),
                    'files': extracted_files
                }
                
                return self.create_result_dict(content)
                
        except Exception as e:
            self.logger.error(f"TAR.GZ extraction error: {e}")
            return self.create_result_dict(
                content={'error': str(e)},
                status='error',
                error_message=str(e)
            )
