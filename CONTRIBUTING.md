# Contributing to Universal Document Extractor

First off, thank you for considering contributing to Universal Document Extractor! It's people like you that make this tool better for everyone.

## 🎯 Ways to Contribute

### 1. Report Bugs
- Use the GitHub issue tracker
- Include OS, Python version, and error messages
- Provide steps to reproduce
- Attach sample files if possible (ensure no sensitive data)

### 2. Suggest Features
- Open an issue with [FEATURE REQUEST] tag
- Describe the feature and its benefits
- Explain use cases

### 3. Submit Code
- Fix bugs
- Add new file type support
- Improve performance
- Enhance UI/UX
- Add tests
- Improve documentation

### 4. Improve Documentation
- Fix typos and errors
- Add examples
- Create tutorials
- Translate documentation

## 🚀 Getting Started

### Development Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/ANY-files-to-JSON.git
cd ANY-files-to-JSON

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install development tools
pip install pytest black flake8 mypy

# 6. Create a branch for your feature
git checkout -b feature/your-feature-name
```

### Development Workflow

1. **Make your changes**
   - Write clean, readable code
   - Follow existing code style
   - Add comments for complex logic
   - Update docstrings

2. **Test your changes**
   ```bash
   python main.py  # Test manually
   pytest  # Run automated tests (when available)
   ```

3. **Format code**
   ```bash
   black .  # Auto-format code
   flake8 .  # Check code style
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: descriptive message"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub

## 📝 Code Guidelines

### Python Style
- Follow PEP 8
- Use meaningful variable names
- Keep functions focused (single responsibility)
- Maximum line length: 100 characters
- Use type hints where possible

### Example:
```python
from pathlib import Path
from typing import Dict, List, Optional

def extract_content(file_path: Path) -> Dict[str, any]:
    """
    Extract content from a file.
    
    Args:
        file_path: Path to the file to extract
        
    Returns:
        Dictionary containing extracted content and metadata
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    # Implementation here
    pass
```

### Commit Messages
Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Formatting changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

Examples:
```
feat: Add support for .epub files
fix: Handle corrupted PDF files gracefully
docs: Update installation instructions
```

## 🏗️ Project Structure

When adding new features, maintain the structure:

```
ANY-files-to-JSON/
├── extractor/          # Add new extractors here
│   └── your_extractor.py
├── gui/                # UI improvements
├── utils/              # Utility functions
├── tests/              # Add tests here
└── docs/               # Documentation
```

### Adding a New File Type Extractor

1. Create extractor in `extractor/` folder:
```python
# extractor/epub_extractor.py
from extractor.base_extractor import BaseExtractor
from pathlib import Path

class EPUBExtractor(BaseExtractor):
    """Extract content from EPUB files"""
    
    def extract(self) -> dict:
        """Extract content from EPUB file"""
        # Your implementation
        return {
            'text': extracted_text,
            'metadata': metadata
        }
```

2. Add to `extractor/__init__.py`:
```python
from .epub_extractor import EPUBExtractor
```

3. Update `config.py`:
```python
SUPPORTED_EXTENSIONS = {
    # ...
    'ebook': ['.epub', '.mobi'],
}
```

4. Update `main.py` routing:
```python
def get_extractor(file_path: Path):
    ext = file_path.suffix.lower()
    # ...
    elif ext == '.epub':
        return EPUBExtractor(file_path)
```

5. Add to README.md supported formats table

## ✅ Pull Request Process

1. **Before submitting**:
   - Update README.md if needed
   - Add tests for new features
   - Ensure all tests pass
   - Format code with `black`
   - Check for linting errors with `flake8`

2. **PR Description should include**:
   - What changes were made
   - Why the changes are needed
   - How to test the changes
   - Screenshots (for UI changes)
   - Related issues (if any)

3. **Review Process**:
   - Maintainers will review your PR
   - Address any feedback
   - Once approved, PR will be merged

## 🎨 UI/UX Guidelines

- Maintain consistent color scheme (Blue/Green/Red/Orange)
- Use emojis for visual clarity
- Ensure responsive design
- Test on different screen sizes
- Follow existing button styles

## 🧪 Testing

### Manual Testing Checklist
- [ ] Test with various file types
- [ ] Test with large batches (1000+ files)
- [ ] Test error scenarios (corrupted files)
- [ ] Test UI responsiveness
- [ ] Test on clean Windows installation

### Automated Testing (Future)
```python
# tests/test_extractor.py
import pytest
from extractor.pdf_extractor import PDFExtractor

def test_pdf_extraction():
    extractor = PDFExtractor(Path('test.pdf'))
    result = extractor.extract()
    assert result['extraction_status'] == 'success'
    assert 'text' in result
```

## 📚 Documentation

When adding features, update:
- README.md - Main documentation
- Docstrings - In-code documentation
- CHANGELOG.md - Version history
- Comments - Complex logic explanations

## 🐛 Bug Reports

Good bug reports include:
1. **Environment**:
   - OS version
   - Python version
   - Installed packages (`pip list`)
   
2. **Steps to reproduce**:
   - Exact steps to trigger the bug
   - Sample files (if applicable)
   
3. **Expected vs Actual**:
   - What should happen
   - What actually happens
   
4. **Logs**:
   - Error messages
   - Screenshots
   - Stack traces

## 💡 Feature Requests

Good feature requests include:
1. **Problem**: What problem does it solve?
2. **Solution**: How should it work?
3. **Alternatives**: What alternatives have you considered?
4. **Use Cases**: Real-world examples
5. **Priority**: How important is this?

## 📞 Questions?

- Open a GitHub Discussion
- Check existing issues
- Read the documentation

## 🏆 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in commits

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing! 🎉
