# ============================================================================
# TEXT EXTRACTOR - Extract plain text files
# ============================================================================

from .base_extractor import BaseExtractor
from typing import Dict, Any
import logging

class TextExtractor(BaseExtractor):
    """Extract content from plain text files"""
    
    def extract(self) -> Dict[str, Any]:
        """
        Extract text content with encoding detection and large file support
        
        Returns:
            Dictionary with text content and metadata
        """
        try:
            # Check file size for large file handling
            file_size_mb = self.file_path.stat().st_size / (1024 * 1024)
            if file_size_mb > 50:
                self.logger.info(f"Processing large text file: {file_size_mb:.2f} MB")
            
            # Read file with auto-detected encoding
            text_content = self.read_file_content()
            
            # Basic text statistics
            lines = text_content.split('\n')
            words = text_content.split()
            
            # Detect file type for specialized parsing
            ext = self.file_path.suffix.lower()
            
            content = {
                'text': text_content,
                'lines': len(lines),
                'words': len(words),
                'characters': len(text_content),
                'file_size_mb': round(file_size_mb, 2),
                'file_type': ext[1:] if ext else 'txt',
                'extraction_method': 'plain_text_with_encoding_detection'
            }
            
            # Add specialized parsing for certain file types
            if ext == '.csv':
                content['csv_data'] = self._parse_csv(text_content)
            elif ext in ['.json', '.jsonl', '.jsn']:
                content['json_data'] = self._parse_json(text_content)
            elif ext == '.xml':
                content['xml_structure'] = self._parse_xml_simple(text_content)
            elif ext == '.log':
                content['log_entries'] = self._parse_log(text_content)
            
            return self.create_result_dict(content)
            
        except Exception as e:
            self.logger.error(f"Text extraction failed: {e}")
            return self.create_result_dict(
                content={'error': str(e)},
                status='error',
                error_message=str(e)
            )
    
    def _parse_csv(self, content: str) -> Dict:
        """Parse CSV content"""
        try:
            import csv
            from io import StringIO
            
            reader = csv.DictReader(StringIO(content))
            rows = list(reader)
            
            return {
                'headers': reader.fieldnames,
                'row_count': len(rows),
                'data': rows[:100]  # First 100 rows to avoid huge JSONs
            }
        except Exception as e:
            self.logger.warning(f"CSV parsing failed: {e}")
            return {'error': str(e)}
    
    def _parse_json(self, content: str) -> Any:
        """Parse JSON content"""
        try:
            import json
            return json.loads(content)
        except Exception as e:
            self.logger.warning(f"JSON parsing failed: {e}")
            return {'error': str(e)}
    
    def _parse_xml_simple(self, content: str) -> Dict:
        """Simple XML structure extraction"""
        import re
        tags = re.findall(r'<(\w+)', content)
        unique_tags = sorted(set(tags))
        return {
            'root_tags': unique_tags[:20],  # Top 20 tags
            'total_tags': len(tags)
        }
    
    def _parse_log(self, content: str) -> Dict:
        """Parse log file"""
        lines = content.split('\n')
        return {
            'total_lines': len(lines),
            'first_line': lines[0] if lines else '',
            'last_line': lines[-1] if lines else '',
            'sample_lines': lines[:10]  # First 10 lines
        }
