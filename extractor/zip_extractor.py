# ============================================================================
# ZIP EXTRACTOR - Recursive ZIP file extraction
# ============================================================================

from .base_extractor import BaseExtractor
from typing import Dict, Any, List
import logging
import zipfile
import tempfile
import shutil
from pathlib import Path

class ZIPExtractor(BaseExtractor):
    """Extract and process ZIP archives recursively"""
    
    def __init__(self, file_path: Path, depth: int = 0):
        super().__init__(file_path)
        self.depth = depth  # Track nesting level
    
    def extract(self) -> Dict[str, Any]:
        """
        Extract ZIP and process all contents recursively
        
        Returns:
            Dictionary with extracted files and their processed content
        """
        from config import Config
        
        # Check depth limit
        if self.depth >= Config.MAX_ZIP_DEPTH:
            return self.create_result_dict(
                content={'warning': f'Max ZIP nesting depth ({Config.MAX_ZIP_DEPTH}) reached'},
                status='partial'
            )
        
        try:
            # Create temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Extract ZIP
                with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                    zip_info = self._get_zip_info(zip_ref)
                
                # Process all extracted files
                extracted_files = self._process_extracted_files(temp_path)
                
                content = {
                    'zip_info': zip_info,
                    'depth_level': self.depth,
                    'extracted_files': extracted_files,
                    'extraction_method': 'zipfile_recursive'
                }
                
                return self.create_result_dict(content)
        
        except zipfile.BadZipFile:
            error_msg = "Invalid or corrupted ZIP file"
            self.logger.error(error_msg)
            return self.create_result_dict(
                content={'error': error_msg},
                status='error',
                error_message=error_msg
            )
        except Exception as e:
            self.logger.error(f"ZIP extraction failed: {e}")
            return self.create_result_dict(
                content={'error': str(e)},
                status='error',
                error_message=str(e)
            )
    
    def _get_zip_info(self, zip_ref: zipfile.ZipFile) -> Dict:
        """Get ZIP metadata"""
        file_list = zip_ref.namelist()
        return {
            'total_files': len(file_list),
            'file_list': file_list,
            'comment': zip_ref.comment.decode('utf-8', errors='ignore') if zip_ref.comment else ''
        }
    
    def _process_extracted_files(self, extract_dir: Path) -> List[Dict]:
        """Process all extracted files"""
        from config import Config
        from . import (PDFExtractor, ImageExtractor, DOCXExtractor,
                       MarkdownExtractor, TextExtractor)
        
        processed_files = []
        
        # Recursively find all files
        for file_path in extract_dir.rglob('*'):
            if file_path.is_file():
                try:
                    # Get file extension
                    ext = file_path.suffix.lower()
                    
                    # Choose appropriate extractor
                    extractor = None
                    
                    if ext == '.zip':
                        # Recursive ZIP extraction
                        extractor = ZIPExtractor(file_path, depth=self.depth + 1)
                    elif ext == '.pdf':
                        extractor = PDFExtractor(file_path)
                    elif ext in Config.SUPPORTED_EXTENSIONS['images']:
                        extractor = ImageExtractor(file_path)
                    elif ext == '.docx':
                        extractor = DOCXExtractor(file_path)
                    elif ext == '.md':
                        extractor = MarkdownExtractor(file_path)
                    elif ext in Config.SUPPORTED_EXTENSIONS['text']:
                        extractor = TextExtractor(file_path)
                    
                    # Extract content
                    if extractor:
                        result = extractor.safe_extract()
                        processed_files.append({
                            'relative_path': str(file_path.relative_to(extract_dir.parent)),
                            'extraction_result': result
                        })
                    else:
                        # Unknown file type
                        processed_files.append({
                            'relative_path': str(file_path.relative_to(extract_dir.parent)),
                            'status': 'skipped',
                            'reason': f'Unsupported file type: {ext}'
                        })
                
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {e}")
                    processed_files.append({
                        'relative_path': str(file_path.relative_to(extract_dir.parent)),
                        'status': 'error',
                        'error': str(e)
                    })
        
        return processed_files
