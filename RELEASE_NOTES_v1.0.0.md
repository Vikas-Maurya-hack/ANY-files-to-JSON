# 🎉 Universal Document Extractor v1.0.0 - Initial Release

**Release Date**: November 8, 2025  
**Build**: v1.0.0  
**Platform**: Windows 7/8/10/11 (64-bit)

---

## 📥 Download

### Standalone Executable (Recommended)
- **File**: `DocumentExtractor.exe`
- **Size**: 84.82 MB (88,962,353 bytes)
- **SHA256**: `008D96819575DEE3E1B93E5A0E751D64E4EBC6C09C24E9D6B12E89F76A04C5B7`

**No Python installation required!** Just download and run.

### Verify Download (Optional but Recommended)
```powershell
# Check SHA256 checksum
Get-FileHash -Algorithm SHA256 "DocumentExtractor.exe"

# Should match: 008D96819575DEE3E1B93E5A0E751D64E4EBC6C09C24E9D6B12E89F76A04C5B7
```

---

## 🚀 Quick Start

1. **Download** `DocumentExtractor.exe` from the Assets section below
2. **Double-click** to launch (if Windows blocks it, right-click → Properties → Unblock)
3. **Select** files or folder using the modern GUI
4. **Click** "▶ Start Extraction"
5. **Find** your JSON output in `D:\extracted_data\`

---

## ✨ Key Features

### 🎨 Modern User Interface
- Beautiful blue gradient header with emoji icons
- Large, accessible buttons for easy interaction
- Real-time progress bar with percentage display
- Color-coded activity log (🟢 Success / 🔴 Error / 🟠 Warning)
- Live statistics (speed, ETA, success/failed counts)
- Dark footer status bar
- Responsive design (1100x800 default, resizable)

### 📦 Comprehensive File Support (80+ Formats)

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
| **Database** | `.sql`, `.graphql`, `.prisma` |

### ⚡ Performance & Features
- **Multi-threaded**: 8 workers by default (configurable)
- **Fast Processing**: 50-200 files/second depending on type
- **Smart Detection**: Automatic file type identification
- **Error Handling**: Gracefully skips unsupported files, continues processing
- **Archive Support**: Automatically extracts ZIP, 7Z, RAR, TAR, GZIP and processes contents
- **Metadata Rich**: MD5 checksums, timestamps, file info, document properties
- **100% Accurate**: Preserves original content without modification

---

## 📋 What Gets Extracted

### Markdown Files
- Raw markdown text
- Converted HTML
- Frontmatter (YAML/TOML)
- Headings structure
- Table of contents
- Code blocks

### PDF Files
- Full text content
- Metadata (author, title, subject, creator)
- Page count
- Encryption status
- PDF version

### Word Documents (.docx, .doc, .odt, .rtf)
- Text content
- Paragraphs structure
- Tables (if any)
- Document properties
- Core metadata

### Images (with Tesseract OCR - optional)
- Extracted text via OCR
- Image dimensions
- Format and mode
- File size

### Code & Text Files
- Full source code/text
- Encoding detection
- Line count
- Language identification

### Archives
- Automatically extracted
- All nested files processed
- Archive type and compression info

---

## 🛠️ Technical Specifications

### Requirements
- **OS**: Windows 7/8/10/11 (64-bit)
- **RAM**: 4GB minimum (8GB recommended for large batches)
- **Disk**: 100MB free space
- **Optional**: Tesseract OCR for image text extraction

### Bundled Dependencies
- PyPDF2 3.0.1 (PDF extraction)
- pdfplumber 0.11.8 (Advanced PDF parsing)
- Pillow 12.0.0 (Image processing)
- pytesseract 0.3.13 (OCR wrapper)
- python-docx 1.2.0 (Word documents)
- markdown 3.10 (Markdown conversion)
- opencv-python 4.12.0 (Image analysis)
- chardet 5.2.0 (Encoding detection)
- py7zr 1.0.0 (7Z archives)
- rarfile 4.2 (RAR archives)
- And more... (all bundled, no installation needed!)

### Output Format
- **Format**: JSON
- **Naming**: `extraction_YYYYMMDD_HHMMSS.json`
- **Location**: `D:\extracted_data\`
- **Structure**: Comprehensive metadata + content for each file
- **Encoding**: UTF-8 with Unicode support

---

## 📊 Performance Benchmarks

Tested on: Intel i7-9700K, 16GB RAM, SSD

| File Type | Speed (files/sec) | Notes |
|-----------|------------------|-------|
| Text Files | ~200 | Very fast |
| Markdown | ~150 | Includes HTML conversion |
| Code Files | ~180 | Plain text extraction |
| PDF (text) | ~50 | Depends on page count |
| PDF (scanned) | ~10 | With OCR enabled |
| DOCX | ~80 | Includes metadata |
| Images | ~30 | With Tesseract OCR |

**Batch Processing:**
- 1,000 files: ~2-5 minutes
- 10,000 files: ~20-40 minutes

---

## 🎯 Perfect For

✅ **AI Training Data** - Prepare datasets for LLMs  
✅ **Document Migration** - Convert legacy documents to JSON  
✅ **Content Analysis** - Analyze large document collections  
✅ **Archive Processing** - Extract from ZIP/RAR/7Z/TAR  
✅ **Code Analysis** - Process source code repositories  
✅ **Knowledge Bases** - Build searchable document databases  

---

## ⚠️ Known Limitations

- Windows only (Linux/Mac support coming in v1.1)
- Image OCR requires Tesseract installation (optional - images are skipped gracefully without it)
- Encrypted PDFs are skipped
- Password-protected archives are skipped
- Very large files (>500MB) may require increased memory

---

## 🆘 Troubleshooting

**Windows blocks the executable?**
- Right-click → Properties → Check "Unblock" → Apply → OK

**Images showing "Tesseract not installed"?**
- This is normal if Tesseract isn't installed
- Images will be skipped, all other files process fine
- To enable OCR: Download from https://github.com/UB-Mannheim/tesseract/wiki

**Extraction is slow?**
- Close other applications
- Increase `MAX_THREADS` in config.py (if running from source)
- Process files locally, not over network

---

## 📝 License

MIT License - Free for personal and commercial use

---

## 🙏 Acknowledgments

Built with amazing open-source libraries:
- PyPDF2, pdfplumber, python-docx, Pillow, pytesseract
- py7zr, rarfile, markdown, opencv-python, chardet
- PyInstaller (for creating the standalone executable)

---

## 🔮 What's Next?

### Planned for v1.1
- Linux and macOS support
- Command-line interface (CLI)
- Resume interrupted extractions
- Export to CSV, Excel, XML

### Planned for v1.2
- Cloud storage integration (Google Drive, Dropbox)
- Database output (MongoDB, PostgreSQL)
- Web-based UI

### Planned for v2.0
- Plugin system
- AI-powered content analysis
- REST API

---

## 📞 Support

- **Issues**: https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON/issues
- **Discussions**: https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON/discussions
- **Documentation**: https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON#readme

---

## ⭐ If you find this useful, please star the repo!

**Made with ❤️ for the AI and Data Science Community**

---

**Full Changelog**: https://github.com/Vikas-Maurya-hack/ANY-files-to-JSON/blob/main/CHANGELOG.md
