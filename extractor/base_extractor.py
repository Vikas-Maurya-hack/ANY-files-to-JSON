# ============================================================================
# BASE EXTRACTOR - Foundation for all extractors
# ============================================================================

import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class BaseExtractor:
    """
    Base class for all document extractors.
    Provides common functionality for metadata extraction, error handling, etc.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize extractor with file path
        
        Args:
            file_path: Full path to file to extract
        """
        self.file_path = Path(file_path)
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Validate file exists
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def extract(self) -> Dict[str, Any]:
        """
        Main extraction method - to be implemented by subclasses
        
        Returns:
            Dictionary with extracted content and metadata
        """
        raise NotImplementedError("Subclasses must implement extract()")
    
    def get_base_metadata(self) -> Dict[str, Any]:
        """
        Extract common file metadata
        
        Returns:
            Dictionary with file metadata
        """
        try:
            stat = self.file_path.stat()
            
            metadata = {
                'file_name': self.file_path.name,
                'file_path': str(self.file_path.absolute()),
                'file_size_bytes': stat.st_size,
                'file_extension': self.file_path.suffix.lower(),
                'created_date': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified_date': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed_date': datetime.fromtimestamp(stat.st_atime).isoformat(),
            }
            
            # Add MD5 checksum if enabled
            from config import Config
            if Config.CALCULATE_CHECKSUMS:
                metadata['md5_checksum'] = self.calculate_md5()
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"Error extracting metadata from {self.file_path}: {e}")
            return {
                'file_name': self.file_path.name,
                'file_path': str(self.file_path.absolute()),
                'metadata_error': str(e)
            }
    
    def calculate_md5(self) -> str:
        """
        Calculate MD5 checksum of file
        
        Returns:
            MD5 hash as hex string
        """
        try:
            md5_hash = hashlib.md5()
            with open(self.file_path, 'rb') as f:
                # Read in chunks for memory efficiency
                for chunk in iter(lambda: f.read(4096), b''):
                    md5_hash.update(chunk)
            return md5_hash.hexdigest()
        except Exception as e:
            self.logger.error(f"Error calculating MD5 for {self.file_path}: {e}")
            return "error_calculating_checksum"
    
    def read_file_content(self, encoding: Optional[str] = None) -> str:
        """
        Read file content with encoding detection
        
        Args:
            encoding: Specific encoding to use, or None for auto-detect
            
        Returns:
            File content as string
        """
        from config import Config
        
        if encoding:
            encodings_to_try = [encoding]
        elif Config.AUTO_DETECT_ENCODING:
            # Try to detect encoding
            import chardet
            with open(self.file_path, 'rb') as f:
                raw_data = f.read()
                detected = chardet.detect(raw_data)
                encodings_to_try = [detected['encoding']] + Config.FALLBACK_ENCODINGS
        else:
            encodings_to_try = Config.FALLBACK_ENCODINGS
        
        # Try each encoding until one works
        for enc in encodings_to_try:
            try:
                with open(self.file_path, 'r', encoding=enc) as f:
                    content = f.read()
                self.logger.debug(f"Successfully read {self.file_path} with encoding: {enc}")
                return content
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                self.logger.error(f"Error reading file with {enc}: {e}")
                continue
        
        # If all encodings fail, read as binary and return hex
        self.logger.warning(f"Could not decode {self.file_path} with any encoding, reading as binary")
        with open(self.file_path, 'rb') as f:
            return f"<binary_content>{f.read().hex()}</binary_content>"
    
    def create_result_dict(self, content: Any, status: str = "success", 
                          error_message: Optional[str] = None) -> Dict[str, Any]:
        """
        Create standardized result dictionary
        
        Args:
            content: Extracted content
            status: Extraction status (success/error/partial)
            error_message: Error message if applicable
            
        Returns:
            Standardized result dictionary
        """
        import uuid
        
        result = {
            'file_id': str(uuid.uuid4()),
            **self.get_base_metadata(),
            'content': content,
            'extraction_status': status,
            'extraction_timestamp': datetime.now().isoformat()
        }
        
        if error_message:
            result['error_message'] = error_message
        
        return result
    
    def safe_extract(self) -> Dict[str, Any]:
        """
        Safely execute extraction with error handling
        
        Returns:
            Result dictionary with content or error
        """
        try:
            return self.extract()
        except Exception as e:
            self.logger.error(f"Extraction failed for {self.file_path}: {e}", exc_info=True)
            return self.create_result_dict(
                content=None,
                status="error",
                error_message=str(e)
            )


# ============================================================================
# USAGE IN SUBCLASSES
# ============================================================================
# class MyExtractor(BaseExtractor):
#     def extract(self):
#         content = self.process_my_file()
#         return self.create_result_dict(content)
# ============================================================================
