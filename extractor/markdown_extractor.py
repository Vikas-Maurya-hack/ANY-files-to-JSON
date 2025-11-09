# ============================================================================
# MARKDOWN EXTRACTOR - Extract content from Markdown files
# ============================================================================

from .base_extractor import BaseExtractor
from typing import Dict, Any, List
import logging

class MarkdownExtractor(BaseExtractor):
    """Extract and parse Markdown files"""
    
    def extract(self) -> Dict[str, Any]:
        """
        Extract Markdown content with frontmatter and structure
        
        Returns:
            Dictionary with raw markdown, HTML, frontmatter, structure
        """
        try:
            import markdown
            import frontmatter
            
            # Read file
            raw_content = self.read_file_content()
            
            # Parse frontmatter (YAML header)
            post = frontmatter.loads(raw_content)
            
            # Convert markdown to HTML
            md = markdown.Markdown(extensions=[
                'meta', 'tables', 'fenced_code', 'codehilite',
                'toc', 'nl2br', 'sane_lists'
            ])
            html_content = md.convert(post.content)
            
            # Extract structure (headings)
            headings = self._extract_headings(post.content)
            
            # Extract code blocks
            code_blocks = self._extract_code_blocks(post.content)
            
            content = {
                'raw_markdown': raw_content,
                'frontmatter': dict(post.metadata) if post.metadata else {},
                'body_markdown': post.content,
                'html': html_content,
                'headings': headings,
                'code_blocks': code_blocks,
                'toc': md.toc if hasattr(md, 'toc') else '',
                'extraction_method': 'python-markdown_with_frontmatter'
            }
            
            return self.create_result_dict(content)
            
        except ImportError as e:
            error_msg = f"Missing dependency: {e}. Install: pip install markdown python-frontmatter"
            self.logger.error(error_msg)
            # Fallback to plain text
            return self.create_result_dict(
                content={
                    'raw_markdown': self.read_file_content(),
                    'extraction_method': 'plain_text_fallback'
                }
            )
        except Exception as e:
            self.logger.error(f"Markdown extraction failed: {e}")
            return self.create_result_dict(
                content={'error': str(e), 'raw_text': self.read_file_content()},
                status='partial',
                error_message=str(e)
            )
    
    def _extract_headings(self, content: str) -> List[Dict]:
        """Extract all headings with levels"""
        import re
        headings = []
        
        # Match markdown headings (# Header, ## Header, etc.)
        pattern = r'^(#{1,6})\s+(.+)$'
        
        for line_num, line in enumerate(content.split('\n'), 1):
            match = re.match(pattern, line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append({
                    'line': line_num,
                    'level': level,
                    'text': text
                })
        
        return headings
    
    def _extract_code_blocks(self, content: str) -> List[Dict]:
        """Extract code blocks"""
        import re
        code_blocks = []
        
        # Match fenced code blocks
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for idx, match in enumerate(matches, 1):
            language = match.group(1) or 'text'
            code = match.group(2).strip()
            code_blocks.append({
                'index': idx,
                'language': language,
                'code': code
            })
        
        return code_blocks
