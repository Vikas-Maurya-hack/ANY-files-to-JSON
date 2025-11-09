#!/usr/bin/env python
# ============================================================================
# VALIDATION SCRIPT - Test all components before running
# ============================================================================

import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def print_check(name, status, message=""):
    symbol = "✓" if status else "✗"
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol}{reset} {name:<40} {message}")

def main():
    print_header("UNIVERSAL DOCUMENT EXTRACTOR - VALIDATION REPORT")
    
    all_passed = True
    
    # ========================================================================
    # 1. PYTHON VERSION CHECK
    # ========================================================================
    print_header("1. Python Environment")
    
    py_version = sys.version_info
    version_ok = py_version >= (3, 8)
    print_check("Python Version", version_ok, 
                f"{py_version.major}.{py_version.minor}.{py_version.micro}")
    all_passed &= version_ok
    
    # ========================================================================
    # 2. PACKAGE IMPORTS
    # ========================================================================
    print_header("2. Required Packages")
    
    packages = {
        'PyPDF2': 'PyPDF2',
        'pdfplumber': 'pdfplumber',
        'Pillow': 'PIL',
        'pytesseract': 'pytesseract',
        'python-docx': 'docx',
        'markdown': 'markdown',
        'python-frontmatter': 'frontmatter',
        'opencv-python': 'cv2',
        'chardet': 'chardet',
        'tqdm': 'tqdm',
        'colorlog': 'colorlog',
        'tkinter': 'tkinter'
    }
    
    for name, import_name in packages.items():
        try:
            __import__(import_name)
            print_check(name, True, "Installed")
        except ImportError as e:
            print_check(name, False, f"MISSING: {e}")
            all_passed = False
    
    # ========================================================================
    # 3. PROJECT MODULES
    # ========================================================================
    print_header("3. Project Modules")
    
    modules = [
        ('config', 'Configuration'),
        ('extractor.base_extractor', 'Base Extractor'),
        ('extractor.pdf_extractor', 'PDF Extractor'),
        ('extractor.image_extractor', 'Image Extractor'),
        ('extractor.docx_extractor', 'DOCX Extractor'),
        ('extractor.markdown_extractor', 'Markdown Extractor'),
        ('extractor.zip_extractor', 'ZIP Extractor'),
        ('extractor.text_extractor', 'Text Extractor'),
        ('utils.logger', 'Logger Utility'),
        ('utils.progress', 'Progress Tracker'),
        ('utils.file_scanner', 'File Scanner'),
        ('gui.main_window', 'GUI Window'),
    ]
    
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print_check(display_name, True, "OK")
        except Exception as e:
            print_check(display_name, False, f"ERROR: {e}")
            all_passed = False
    
    # ========================================================================
    # 4. EXTRACTOR CLASSES
    # ========================================================================
    print_header("4. Extractor Classes")
    
    try:
        from extractor import (PDFExtractor, ImageExtractor, DOCXExtractor,
                               MarkdownExtractor, ZIPExtractor, TextExtractor)
        
        extractors = [
            (PDFExtractor, 'PDFExtractor'),
            (ImageExtractor, 'ImageExtractor'),
            (DOCXExtractor, 'DOCXExtractor'),
            (MarkdownExtractor, 'MarkdownExtractor'),
            (ZIPExtractor, 'ZIPExtractor'),
            (TextExtractor, 'TextExtractor'),
        ]
        
        for extractor_class, name in extractors:
            has_extract = hasattr(extractor_class, 'extract')
            print_check(name, has_extract, 
                       "Has extract() method" if has_extract else "Missing extract()")
            all_passed &= has_extract
    
    except Exception as e:
        print_check("Extractor Import", False, f"ERROR: {e}")
        all_passed = False
    
    # ========================================================================
    # 5. CONFIGURATION
    # ========================================================================
    print_header("5. Configuration Settings")
    
    try:
        from config import Config
        
        checks = [
            (hasattr(Config, 'OUTPUT_FOLDER'), 'OUTPUT_FOLDER defined'),
            (hasattr(Config, 'MAX_THREADS'), 'MAX_THREADS defined'),
            (hasattr(Config, 'SUPPORTED_EXTENSIONS'), 'SUPPORTED_EXTENSIONS defined'),
            (hasattr(Config, 'TESSERACT_PATH'), 'TESSERACT_PATH defined'),
            (hasattr(Config, 'DEBUG_MODE'), 'DEBUG_MODE defined'),
        ]
        
        for status, msg in checks:
            print_check(msg, status)
            all_passed &= status
        
        if hasattr(Config, 'OUTPUT_FOLDER'):
            print(f"    → Output Folder: {Config.OUTPUT_FOLDER}")
        if hasattr(Config, 'MAX_THREADS'):
            print(f"    → Max Threads: {Config.MAX_THREADS}")
    
    except Exception as e:
        print_check("Config Import", False, f"ERROR: {e}")
        all_passed = False
    
    # ========================================================================
    # 6. FILE STRUCTURE
    # ========================================================================
    print_header("6. File Structure")
    
    required_files = [
        'main.py',
        'config.py',
        'requirements.txt',
        'README.md',
        'extractor/__init__.py',
        'extractor/base_extractor.py',
        'extractor/pdf_extractor.py',
        'extractor/image_extractor.py',
        'extractor/docx_extractor.py',
        'extractor/markdown_extractor.py',
        'extractor/zip_extractor.py',
        'extractor/text_extractor.py',
        'gui/__init__.py',
        'gui/main_window.py',
        'utils/__init__.py',
        'utils/logger.py',
        'utils/progress.py',
        'utils/file_scanner.py',
    ]
    
    for file_path in required_files:
        exists = Path(file_path).exists()
        print_check(file_path, exists, "Found" if exists else "MISSING")
        all_passed &= exists
    
    # ========================================================================
    # 7. DIRECTORIES
    # ========================================================================
    print_header("7. Output Directories")
    
    try:
        from config import Config
        output_dir = Path(Config.OUTPUT_FOLDER)
        output_exists = output_dir.exists()
        print_check("Output Directory", output_exists, str(output_dir))
        
        if output_exists:
            print(f"    → Writable: {os.access(output_dir, os.W_OK)}")
    except Exception as e:
        print_check("Output Directory", False, f"ERROR: {e}")
        all_passed = False
    
    # ========================================================================
    # 8. TESSERACT OCR
    # ========================================================================
    print_header("8. Tesseract OCR (Optional)")
    
    try:
        from config import Config
        tesseract_exists = Path(Config.TESSERACT_PATH).exists()
        print_check("Tesseract Installed", tesseract_exists, 
                   Config.TESSERACT_PATH if tesseract_exists else "NOT FOUND")
        
        if not tesseract_exists:
            print("    ⚠ WARNING: Image OCR will not work without Tesseract")
            print("    → Download from: https://github.com/UB-Mannheim/tesseract/wiki")
    except Exception as e:
        print_check("Tesseract Check", False, f"ERROR: {e}")
    
    # ========================================================================
    # 9. GUI TEST
    # ========================================================================
    print_header("9. GUI Availability")
    
    try:
        import tkinter
        root = tkinter.Tk()
        root.withdraw()
        root.destroy()
        print_check("tkinter GUI", True, "Available")
    except Exception as e:
        print_check("tkinter GUI", False, f"ERROR: {e}")
        all_passed = False
    
    # ========================================================================
    # FINAL RESULT
    # ========================================================================
    print_header("VALIDATION RESULT")
    
    if all_passed:
        print("\n✓✓✓ ALL CHECKS PASSED! Application is ready to run. ✓✓✓\n")
        print("To start the application:")
        print("  venv\\Scripts\\python.exe main.py")
        print("\nOr use CLI mode:")
        print('  venv\\Scripts\\python.exe main.py "E:\\YourFolder"')
        return 0
    else:
        print("\n✗✗✗ SOME CHECKS FAILED! Please fix errors above. ✗✗✗\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
