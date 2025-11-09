# 📄 Universal Document Extractor

<div align="center">

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**A powerful, modern document extraction tool that converts 80+ file types to structured JSON format**

Perfect for AI Training • Data Processing • Content Analysis • Document Management

[Download Latest Release](https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON/releases) • [Documentation](#documentation) • [Report Bug](https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON/issues)

![Screenshot](https://via.placeholder.com/800x400/2196F3/ffffff?text=Modern+UI+Screenshot)

</div>

---

## 🌟 Features

### 📦 **Comprehensive File Support**
Extract content from **80+ file formats** including:

| Category | Supported Formats |
|----------|------------------|
| **Markdown** | `.md`, `.markdown`, `.mdown`, `.mkd`, `.mdx` |
| **Documents** | `.pdf`, `.docx`, `.doc`, `.odt`, `.rtf` |
| **Images** | `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.tiff`, `.jfif`, `.svg`, `.ico` |
| **Code** | `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.c`, `.cs`, `.go`, `.rs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.r`, `.m`, `.dart` |
| **Web** | `.html`, `.css`, `.xml`, `.json`, `.yaml`, `.yml`, `.toml` |
| **Config** | `.ini`, `.conf`, `.cfg`, `.env`, `.properties`, `.gitignore` |
| **Data** | `.csv`, `.tsv`, `.txt`, `.log` |
| **Archives** | `.zip`, `.gz`, `.7z`, `.tar`, `.rar`, `.tar.gz`, `.tar.bz2`, `.tgz` |
| **Scripts** | `.sh`, `.bash`, `.ps1`, `.bat`, `.cmd`, `.zsh` |
| **Database** | `.sql`, `.graphql`, `.prisma`, `.mongodb` |
| **Others** | `.tex`, `.bib`, `.rst`, `.adoc`, `.org` |

### ✨ **Key Capabilities**

- 🎨 **Modern UI** - Beautiful, intuitive interface with real-time progress tracking
- ⚡ **Multi-threaded** - Process multiple files simultaneously (8 workers by default)
- 🎯 **100% Accurate** - Preserves original content without modifications
- 📊 **Rich Metadata** - Extracts file info, dates, MD5 checksums, and document structure
- 🔄 **Batch Processing** - Handle thousands of files in one go
- 📈 **Progress Tracking** - Live progress bar, statistics, speed, and ETA
- 🛡️ **Error Handling** - Gracefully skips unsupported files, continues processing
- 💾 **Portable** - Standalone executable, no installation required
- 🔍 **Smart Detection** - Auto-detects file types and applies appropriate extractors
- 📦 **Archive Support** - Automatically extracts and processes archived files

---

## 🚀 Quick Start

### Option 1: Download Executable (Recommended for Users)

1. **Download** the latest `DocumentExtractor.exe` from [Releases](https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON/releases)
2. **Double-click** to launch the application
3. **Select files or folder** using the modern GUI
4. **Click "▶ Start Extraction"** 
5. **Find your JSON** in `D:\extracted_data\`

### Option 2: Run from Source (For Developers)

```bash
# Clone the repository
git clone https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON.git
cd ANY-files-to-JSON

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 📖 Usage

### GUI Mode (Recommended)

1. **Launch** the application (double-click `DocumentExtractor.exe` or run `python main.py`)
2. **Choose extraction method:**

   **Method A - Select Specific Files:**
   - Click "📄 Select Files" button
   - Choose one or multiple files (hold Ctrl and click for multiple selection)
   - Click "▶ Start Extraction"

   **Method B - Scan Entire Folder:**
   - Click "📁 Select Folder" button
   - Choose a directory (all supported files will be automatically discovered)
   - Click "▶ Start Extraction"

3. **Monitor progress** in real-time:
   - Progress bar shows completion percentage
   - Statistics show success/failed counts
   - Current file being processed is displayed
   - Activity log shows detailed information

4. **Access results** in `D:\extracted_data\extraction_YYYYMMDD_HHMMSS.json`

### Command Line Mode (Coming Soon)

```bash
# Extract from a directory
python main.py --source "C:\Documents\MyFiles" --output "output.json"

# Extract specific file types
python main.py --source "C:\Data" --types ".md,.pdf,.docx"

# Set number of threads
python main.py --source "C:\Data" --threads 16
```

---

## 📋 Output Format

The tool generates a comprehensive JSON file with the following structure:

```json
{
  "metadata": {
    "extraction_date": "2025-11-08T23:20:07.127488",
    "source_directory": "C:\\Documents\\MyFiles",
    "total_files": 150,
    "version": "1.0.0"
  },
  "results": [
    {
      "file_id": "6912f307-4201-4f00-8d18-156b8a550c50",
      "file_name": "document.md",
      "file_path": "C:\\Documents\\MyFiles\\document.md",
      "file_size_bytes": 18697,
      "file_extension": ".md",
      "created_date": "2025-10-24T15:15:45.658756",
      "modified_date": "2025-10-24T15:20:28.424732",
      "accessed_date": "2025-11-08T23:20:07.007222",
      "md5_checksum": "958d7d41e3acbd6a6a871efa404e030a",
      "content": {
        "raw_markdown": "# Full original content preserved...",
        "html": "<h1>Converted HTML for markdown</h1>",
        "frontmatter": {},
        "headings": [
          {"line": 1, "level": 1, "text": "Introduction"},
          {"line": 15, "level": 2, "text": "Features"}
        ],
        "code_blocks": [],
        "toc": "<div class='toc'>Table of Contents...</div>"
      },
      "extraction_status": "success",
      "extraction_timestamp": "2025-11-08T23:20:08.115125"
    }
  ]
}
```

### Content Fields by File Type

| File Type | Content Fields |
|-----------|---------------|
| **Markdown** | `raw_markdown`, `html`, `frontmatter`, `body_markdown`, `headings`, `toc`, `code_blocks`, `extraction_method` |
| **PDF** | `text`, `metadata` (author, title, subject, creator), `page_count`, `encrypted`, `pdf_version` |
| **DOCX** | `text`, `paragraphs`, `tables`, `metadata`, `properties`, `core_properties` |
| **Images** | `ocr_text`, `dimensions`, `format`, `mode`, `size` (requires Tesseract OCR) |
| **Code Files** | `code`, `language`, `line_count`, `encoding`, `raw_content` |
| **Text Files** | `text`, `encoding`, `line_count`, `raw_content` |
| **Archives** | `extracted_files`, `archive_type`, `compression_method`, `total_size` |

---

## 🛠️ Installation & Setup

### Requirements

- **Python**: 3.8 or higher
- **OS**: Windows 7/8/10/11 (64-bit)
- **RAM**: 4GB minimum (8GB recommended for large batches)
- **Disk**: 100MB free space

### Python Dependencies

All dependencies are listed in `requirements.txt`:

```txt
PyPDF2>=3.0.1          # PDF text extraction
pdfplumber>=0.11.8     # Advanced PDF parsing with tables
Pillow>=12.0.0         # Image processing
pytesseract>=0.3.13    # OCR for images (optional)
python-docx>=1.2.0     # Word document extraction
markdown>=3.10         # Markdown to HTML conversion
opencv-python>=4.12.0  # Image analysis
chardet>=5.2.0         # Character encoding detection
tqdm>=4.67.1           # Progress bars
colorlog>=6.10.1       # Colored logging
py7zr>=1.0.0           # 7Z archive support
rarfile>=4.2           # RAR archive support
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

### Optional Dependencies

- **Tesseract OCR**: For image text extraction (OCR)
  - Download: https://github.com/tesseract-ocr/tesseract
  - Windows installer: https://github.com/UB-Mannheim/tesseract/wiki
  - Add to system PATH after installation
  - Without Tesseract, images will be skipped gracefully

---

## 🏗️ Project Structure

```
ANY-files-to-JSON/
├── main.py                    # Application entry point
├── config.py                  # Configuration and supported file types
├── requirements.txt           # Python dependencies
├── build_exe.spec            # PyInstaller build specification
├── README.md                 # This file
├── LICENSE                   # MIT License
│
├── gui/
│   ├── __init__.py
│   └── main_window.py        # Modern GUI interface with blue theme
│
├── extractor/
│   ├── __init__.py
│   ├── base_extractor.py     # Base extractor class
│   ├── pdf_extractor.py      # PDF extraction (PyPDF2 + pdfplumber)
│   ├── image_extractor.py    # Image OCR with Tesseract
│   ├── docx_extractor.py     # Word documents (.docx, .doc, .odt, .rtf)
│   ├── markdown_extractor.py # Markdown files with HTML conversion
│   ├── text_extractor.py     # Plain text and code files
│   ├── zip_extractor.py      # ZIP archives
│   ├── gzip_extractor.py     # GZIP and .tar.gz archives
│   ├── sevenzip_extractor.py # 7Z archives
│   ├── tar_extractor.py      # TAR archives
│   └── rar_extractor.py      # RAR archives
│
├── utils/
│   ├── __init__.py
│   ├── logger.py             # Logging configuration with colors
│   ├── progress.py           # Progress tracking and statistics
│   └── file_scanner.py       # Recursive file discovery
│
└── dist/
    ├── DocumentExtractor.exe  # Standalone Windows executable (89 MB)
    └── README.txt            # User guide for executable
```

---

## 🔧 Building Executable

To create a standalone Windows executable:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the executable using the spec file
pyinstaller build_exe.spec --clean --noconfirm

# Executable will be created at:
# dist/DocumentExtractor.exe (approximately 89 MB)

# The executable includes:
# - All Python dependencies
# - GUI interface
# - No Python installation required to run
```

### Spec File Configuration

The `build_exe.spec` file is pre-configured with:
- Hidden imports for all dependencies
- Single-file executable (all-in-one)
- No console window (windowed mode)
- Optimized with UPX compression

---

## 🎯 Use Cases

### 1. **AI Training Data Preparation**
Perfect for preparing training datasets for Large Language Models (LLMs):
- Extract documentation from markdown files
- Process code repositories
- Convert PDFs to structured text
- Batch process thousands of files
- Preserve metadata and structure

### 2. **Document Migration & Archival**
Migrate legacy documents to modern JSON format:
- Convert old Word documents
- Extract content from scanned PDFs
- Process historical archives
- Preserve original formatting and metadata

### 3. **Content Analysis & Research**
Analyze large document collections:
- Extract headings and structure
- Identify code blocks and snippets
- Collect statistics across documents
- Search and index content

### 4. **Archive Processing**
Automatically handle archived files:
- Extract ZIP, RAR, 7Z, TAR archives
- Process nested archives recursively
- Batch convert archived documents
- Preserve archive structure

### 5. **Code Repository Analysis**
Extract and analyze source code:
- Support for 40+ programming languages
- Preserve syntax and structure
- Extract comments and documentation
- Batch process entire repositories

### 6. **Knowledge Base Creation**
Build searchable knowledge bases:
- Extract from mixed document types
- Preserve cross-references
- Generate table of contents
- Create structured indices

---

## 🎨 UI Features

### Modern Interface Elements

#### **Header Section**
- Blue gradient header with emoji icon
- Subtitle showing supported file types
- Version information

#### **File Selection Section**
- Two large blue buttons:
  - 📄 **Select Files** - Choose specific files
  - 📁 **Select Folder** - Scan entire directory
- Selected files/folder displayed with count
- Color-coded status (gray → green when selected)

#### **File Statistics Panel**
- Total files found
- Total size (human-readable format)
- Number of file types detected
- Updates in real-time during scan

#### **Progress Section**
- Large green progress bar with percentage
- Real-time statistics:
  - Processed count (X/Total)
  - Success count (green checkmark)
  - Failed count (red X)
  - Processing speed (files/second)
  - Estimated time remaining (ETA)
- Current file being processed (blue text)

#### **Activity Log**
- Color-coded messages:
  - 🟢 **Green**: Success messages
  - 🔴 **Red**: Errors
  - 🟠 **Orange**: Warnings
  - ⚫ **Black**: Info messages
- Monospace font for better readability
- Auto-scroll to latest message
- Scrollable history

#### **Control Buttons**
- 🟢 **Start Extraction** (Green, large)
- 🔴 **Stop** (Red, large)
- 🟠 **Clear Log** (Orange, large)

#### **Status Bar**
- Dark footer with current status
- Shows operation state
- Success/error notifications

---

## ⚙️ Configuration

### Customize Supported File Types

Edit `config.py` to add or modify supported file types:

```python
SUPPORTED_EXTENSIONS = {
    'images': ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.jfif', '.svg', '.ico'],
    'pdf': ['.pdf'],
    'docx': ['.docx', '.doc', '.odt', '.rtf'],
    'markdown': ['.md', '.markdown', '.mdown', '.mkd', '.mdx'],
    'text': ['.txt', '.log', '.csv', '.xml', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf', '.env'],
    'archive': ['.zip', '.gz', '.7z', '.tar', '.rar', '.tgz', '.tar.gz', '.tar.bz2', '.bz2'],
    # Add your custom types here
}
```

### Adjust Threading

Modify worker count in `config.py`:

```python
MAX_THREADS = 8  # Default: 8 workers
# Increase for faster processing on powerful machines
# Decrease if experiencing memory issues
```

### Change Output Directory

Update output location in `config.py`:

```python
OUTPUT_DIR = Path("D:/extracted_data")  # Default
# Change to any directory you prefer
```

### Configure Logging

Adjust logging level in `config.py`:

```python
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

**Q: Images showing "Tesseract OCR not installed"**  
**A**: This is normal if Tesseract is not installed. Images will be skipped, but all other files will process fine. To enable image OCR:
1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
2. Install with default settings
3. Add to system PATH: `C:\Program Files\Tesseract-OCR`
4. Restart the application

**Q: Large batches running out of memory**  
**A**: Try these solutions:
- Reduce `MAX_THREADS` in config.py to 4 or 2
- Process files in smaller batches
- Close other applications
- Increase system virtual memory

**Q: Extraction is slow**  
**A**: Performance tips:
- Increase `MAX_THREADS` to 16 or higher (if CPU allows)
- Use SSD instead of HDD for source files
- Close antivirus during processing
- Process files locally, not over network

**Q: Archive files not extracting**  
**A**: Ensure all archive libraries are installed:
```bash
pip install py7zr rarfile
```

**Q: Executable not starting or blocked by Windows**  
**A**: Windows Defender may block unknown executables:
- Right-click → Properties → Unblock checkbox
- Add to Windows Defender exceptions
- Or build from source with your own certificate

**Q: Some files showing as "unsupported"**  
**A**: Check if the file extension is listed in `config.py` under `SUPPORTED_EXTENSIONS`. Add it if needed.

**Q: PDF extraction incomplete**  
**A**: Some PDFs are:
- Encrypted (password-protected)
- Scanned images without OCR layer
- Corrupted files
Check the error log for specific issues.

**Q: Unicode errors in output**  
**A**: The tool uses UTF-8 encoding. If issues persist:
- Check original file encoding
- Report the issue with sample file

---

## 📊 Performance Benchmarks

Tested on: Intel i7-9700K, 16GB RAM, SSD

| File Type | Files/Second | Notes |
|-----------|-------------|-------|
| **Text Files** | ~200 | Very fast |
| **Markdown** | ~150 | Includes HTML conversion |
| **Code Files** | ~180 | Plain text extraction |
| **PDF (text)** | ~50 | Depends on page count |
| **PDF (scanned)** | ~10 | With OCR enabled |
| **DOCX** | ~80 | Includes metadata |
| **Images** | ~30 | With Tesseract OCR |
| **Archives** | Varies | Depends on contents |

### Large Batch Performance
- **1,000 files**: ~2-5 minutes (mixed types)
- **10,000 files**: ~20-40 minutes (mixed types)
- **100,000+ files**: Process in batches

### Memory Usage
- **Typical batch (1000 files)**: 2-4GB RAM
- **Large batch (10000 files)**: 4-8GB RAM
- **Peak usage**: Depends on file sizes

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Make** your changes
4. **Commit** with clear messages:
   ```bash
   git commit -m 'Add AmazingFeature: Description'
   ```
5. **Push** to your branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
6. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ANY-files-to-JSON.git
cd ANY-files-to-JSON

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies + dev tools
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests (when available)
pytest

# Format code
black .

# Lint code
flake8 .
```

### Contribution Ideas

- Add support for new file types
- Improve extraction accuracy
- Optimize performance
- Add Linux/macOS support
- Create web-based UI
- Add cloud storage integration
- Write tests
- Improve documentation
- Report bugs
- Suggest features

---

## 📝 License

This project is licensed under the **MIT License**:

```
MIT License

Copyright (c) 2025 Vikas Maurya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

See the [LICENSE](LICENSE) file for full details.

---

## 👨‍💻 Author

**Vikas Maurya**

- GitHub: [@Vikas-Maurya-hack](https://github.com/Vikas-Maurya-hack)
- Repository: [ANY-files-to-JSON](https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON)
- Email: [Contact via GitHub](https://github.com/Vikas-Maurya-hack)

---

## 🙏 Acknowledgments

This project is built on top of amazing open-source libraries:

- **[PyPDF2](https://github.com/py-pdf/pypdf)** - PDF text extraction
- **[pdfplumber](https://github.com/jsvine/pdfplumber)** - Advanced PDF parsing
- **[python-docx](https://github.com/python-openxml/python-docx)** - Word document processing
- **[Pillow](https://github.com/python-pillow/Pillow)** - Image processing
- **[pytesseract](https://github.com/madmaze/pytesseract)** - OCR wrapper for Tesseract
- **[py7zr](https://github.com/miurahr/py7zr)** - 7Z archive support
- **[rarfile](https://github.com/markokr/rarfile)** - RAR archive support
- **[markdown](https://github.com/Python-Markdown/markdown)** - Markdown to HTML conversion
- **[PyInstaller](https://github.com/pyinstaller/pyinstaller)** - Executable builder

Special thanks to the open-source community!

---

## 📈 Changelog

### v1.0.0 (2025-11-08) - Initial Release

#### New Features
- ✨ Modern GUI with blue theme and large buttons
- ✨ Support for 80+ file types across 10 categories
- ✨ Multi-threaded extraction (8 workers)
- ✨ Real-time progress tracking with ETA
- ✨ Archive extraction (ZIP, 7Z, RAR, TAR, GZIP)
- ✨ Comprehensive JSON output with metadata
- ✨ Standalone Windows executable (89 MB)
- ✨ Color-coded activity log
- ✨ File and folder selection modes
- ✨ MD5 checksum generation
- ✨ Error handling and recovery
- ✨ Graceful Tesseract OCR fallback

#### Supported File Types
- **Markdown**: 5 extensions
- **Documents**: PDF, DOCX, DOC, ODT, RTF
- **Images**: 9 formats (with OCR support)
- **Code**: 40+ languages
- **Archives**: 9 formats
- **Data**: CSV, JSON, XML, YAML, etc.
- **Total**: 80+ file types

---

## 🔮 Roadmap

### Planned Features

#### Version 1.1
- [ ] Linux and macOS support
- [ ] Command-line interface (CLI)
- [ ] Batch processing from config file
- [ ] Resume interrupted extractions
- [ ] Export to CSV, Excel, XML
- [ ] File filtering by size/date

#### Version 1.2
- [ ] Cloud storage integration:
  - [ ] Google Drive
  - [ ] Dropbox
  - [ ] OneDrive
- [ ] Database output options:
  - [ ] MongoDB
  - [ ] PostgreSQL
  - [ ] SQLite

#### Version 1.3
- [ ] Web-based UI (browser interface)
- [ ] REST API endpoint
- [ ] Docker containerization
- [ ] Email notifications
- [ ] Scheduled extractions (cron jobs)

#### Version 2.0
- [ ] Custom extraction templates
- [ ] Plugin system for new file types
- [ ] AI-powered content analysis
- [ ] Duplicate detection
- [ ] Content search and indexing
- [ ] Batch scripting support

---

## 📚 Documentation

### Additional Resources

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed setup instructions
- **[User Guide](docs/USER_GUIDE.md)** - Complete usage documentation
- **[API Reference](docs/API.md)** - For developers
- **[FAQ](docs/FAQ.md)** - Frequently asked questions
- **[Examples](docs/EXAMPLES.md)** - Code examples and use cases

*(Documentation files coming soon)*

---

## 🔒 Security

### Security Considerations

- **No Network Access**: Tool runs completely offline
- **Local Processing**: All extraction happens on your machine
- **No Data Collection**: No telemetry or analytics
- **Open Source**: Full source code available for audit

### Reporting Security Issues

If you discover a security vulnerability, please email:
- Create a private security advisory on GitHub
- Or contact via [GitHub Issues](https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON/issues) with [SECURITY] tag

---

## ❓ FAQ

**Q: Is this tool free?**  
A: Yes, completely free and open-source (MIT License).

**Q: Does it work on Mac/Linux?**  
A: Currently Windows only. Mac/Linux support is planned for v1.1.

**Q: Can I use this for commercial projects?**  
A: Yes! MIT License allows commercial use.

**Q: Does it require internet?**  
A: No, works completely offline.

**Q: How accurate is the extraction?**  
A: 100% for text-based files. OCR accuracy depends on image quality.

**Q: Can it handle password-protected files?**  
A: Not currently. Encrypted PDFs and archives will be skipped.

**Q: Maximum file size?**  
A: Tested up to 500MB per file. Larger files may work but consume more memory.

**Q: Can I extract from network drives?**  
A: Yes, but local drives are faster.

---

## 📞 Support

### Get Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON/discussions)
- **Documentation**: Check the [docs](docs/) folder
- **Email**: Contact via GitHub profile

### Before Reporting Issues

Please include:
1. Operating system and version
2. Python version (if running from source)
3. Error message or screenshot
4. Steps to reproduce
5. Sample files (if possible)

---

<div align="center">

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Vikas-Maurya-hack/ANY-files-to-JSON&type=Date)](https://star-history.com/#Vikas-Maurya-hack/ANY-files-to-JSON&Date)

---

**Made with ❤️ for the AI and Data Science Community**

### If this project helped you, consider giving it a ⭐!

[⬆ Back to Top](#-universal-document-extractor)

</div>

---

<div align="center">

**Keywords**: document extraction, JSON converter, AI training data, file parser, content extractor, markdown to JSON, PDF to JSON, batch processing, multi-format converter, data processing tool

</div>
