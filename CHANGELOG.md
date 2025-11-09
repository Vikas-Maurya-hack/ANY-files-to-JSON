# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-08

### 🎉 Initial Release

#### Added
- **Modern GUI Interface**
  - Blue gradient header with emoji icons
  - Large, accessible buttons (📄 Select Files, 📁 Select Folder)
  - Real-time progress bar with percentage display
  - Color-coded activity log (Green/Red/Orange/Black)
  - File statistics panel
  - Dark footer status bar
  - Responsive layout (900x700 minimum, 1100x800 default)

- **File Type Support (80+ formats)**
  - Markdown (5 extensions): `.md`, `.markdown`, `.mdown`, `.mkd`, `.mdx`
  - PDF: `.pdf`
  - Word Documents (4 types): `.docx`, `.doc`, `.odt`, `.rtf`
  - Images (9 formats): `.png`, `.jpg`, `.jpeg`, `.bmp`, `.gif`, `.tiff`, `.jfif`, `.svg`, `.ico`
  - Code Files (40+ languages): `.py`, `.js`, `.ts`, `.java`, `.cpp`, `.c`, `.cs`, `.go`, `.rs`, `.php`, `.rb`, `.swift`, `.kt`, and more
  - Web Files: `.html`, `.css`, `.xml`, `.json`, `.yaml`, `.yml`, `.toml`
  - Config Files: `.ini`, `.conf`, `.cfg`, `.env`, `.properties`
  - Data Files: `.csv`, `.tsv`, `.txt`, `.log`
  - Archives (9 formats): `.zip`, `.gz`, `.7z`, `.tar`, `.rar`, `.tgz`, `.tar.gz`, `.tar.bz2`, `.bz2`
  - Scripts: `.sh`, `.bash`, `.ps1`, `.bat`, `.cmd`
  - Database: `.sql`, `.graphql`, `.prisma`

- **Extraction Features**
  - Multi-threaded processing (8 workers default)
  - Real-time progress tracking with ETA
  - MD5 checksum generation for all files
  - Comprehensive metadata extraction (dates, sizes, permissions)
  - Automatic file type detection
  - Error handling with graceful degradation
  - Archive auto-extraction and recursive processing

- **File Type Specific Extractors**
  - **PDF Extractor**: Text extraction, metadata, page count, encryption detection
  - **Image Extractor**: OCR with Tesseract (optional), image metadata
  - **DOCX Extractor**: Text, paragraphs, tables, document properties, fallback for .doc/.odt/.rtf
  - **Markdown Extractor**: Raw markdown, HTML conversion, frontmatter, headings, TOC, code blocks
  - **Text Extractor**: Plain text, encoding detection, line count
  - **ZIP Extractor**: Recursive extraction, nested file processing
  - **GZIP Extractor**: Single files and tar.gz archives
  - **7Z Extractor**: 7-Zip archive support with py7zr
  - **TAR Extractor**: TAR archive processing
  - **RAR Extractor**: RAR archive support with rarfile

- **Output Features**
  - Structured JSON output with complete metadata
  - Timestamped file naming (`extraction_YYYYMMDD_HHMMSS.json`)
  - Preservation of file structure and relationships
  - Human-readable file sizes
  - Extraction status tracking
  - Processing statistics

- **Utilities**
  - Colored logging system with multiple levels
  - Progress tracker with statistics (speed, ETA, counts)
  - Recursive file scanner with filtering
  - Character encoding detection with chardet

- **Standalone Executable**
  - Windows .exe build (89 MB, single file)
  - No Python installation required
  - All dependencies bundled
  - PyInstaller build configuration
  - Optimized with UPX compression

- **Documentation**
  - Comprehensive README.md with examples
  - User guide (README.txt) for executable
  - MIT License
  - Contributing guidelines
  - Changelog

#### Technical Details
- **Language**: Python 3.8+
- **GUI Framework**: Tkinter
- **Threading**: concurrent.futures.ThreadPoolExecutor
- **PDF**: PyPDF2 3.0.1, pdfplumber 0.11.8
- **Images**: Pillow 12.0.0, pytesseract 0.3.13, opencv-python 4.12.0
- **Documents**: python-docx 1.2.0
- **Markdown**: markdown 3.10
- **Archives**: py7zr 1.0.0, rarfile 4.2, built-in zipfile/tarfile/gzip
- **Utilities**: chardet 5.2.0, tqdm 4.67.1, colorlog 6.10.1

#### Performance
- Processing speed: 50-200 files/second (varies by type)
- Memory usage: 2-4GB for typical batches (1000 files)
- Tested with batches of 10,000+ files
- 8 worker threads by default (configurable)

#### Known Limitations
- Windows only (Linux/Mac support planned for v1.1)
- Image OCR requires Tesseract installation (optional)
- Encrypted PDFs are skipped
- Password-protected archives are skipped
- Very large files (>500MB) may require increased memory

---

## [Unreleased]

### Planned for v1.1
- [ ] Linux and macOS support
- [ ] Command-line interface (CLI)
- [ ] Batch processing from config file
- [ ] Resume interrupted extractions
- [ ] Export to CSV, Excel, XML formats
- [ ] File filtering by size/date/type
- [ ] Automated tests with pytest
- [ ] Performance optimizations

### Planned for v1.2
- [ ] Cloud storage integration (Google Drive, Dropbox, OneDrive)
- [ ] Database output options (MongoDB, PostgreSQL, SQLite)
- [ ] Web-based UI (browser interface)
- [ ] Docker containerization

### Planned for v2.0
- [ ] Plugin system for custom extractors
- [ ] AI-powered content analysis
- [ ] REST API endpoint
- [ ] Duplicate detection
- [ ] Content search and indexing
- [ ] Scheduled extractions (cron jobs)

---

## Version History

- **1.0.0** (2025-11-08) - Initial release with 80+ file type support and modern GUI

---

### Legend
- `Added` - New features
- `Changed` - Changes in existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Vulnerability fixes

---

**Note**: This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version (X.0.0) - Incompatible API changes
- MINOR version (0.X.0) - New functionality (backwards compatible)
- PATCH version (0.0.X) - Bug fixes (backwards compatible)
