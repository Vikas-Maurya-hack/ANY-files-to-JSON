# ============================================================================
# CONFIGURATION - Universal Document Extractor
# ============================================================================

import os
from pathlib import Path

class Config:
    """Central configuration for the document extractor"""
    
    # -------------------------------------------------------------------------
    # OUTPUT SETTINGS
    # -------------------------------------------------------------------------
    OUTPUT_DRIVE = "D:\\"
    OUTPUT_FOLDER = os.path.join(OUTPUT_DRIVE, "extracted_data")
    
    # Create output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    # JSON output settings
    JSON_INDENT = 2  # Pretty printing with 2 spaces
    JSON_ENSURE_ASCII = False  # Preserve Unicode characters
    
    # -------------------------------------------------------------------------
    # PROCESSING SETTINGS
    # -------------------------------------------------------------------------
    MAX_THREADS = 8  # Number of parallel processing threads
    CHUNK_SIZE = 100  # Process files in chunks for memory efficiency
    
    # -------------------------------------------------------------------------
    # FILE TYPE SUPPORT
    # -------------------------------------------------------------------------
    SUPPORTED_EXTENSIONS = {
        'images': {'.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.tif', '.webp', '.ico', '.svg', '.jfif', '.jpe', '.jif'},
        'pdf': {'.pdf'},
        'docx': {'.docx', '.doc', '.odt', '.rtf'},
        'markdown': {'.md', '.markdown', '.mdown', '.mkd', '.mdx'},
        'text': {
            # Plain text
            '.txt', '.text', '.log', '.logs',
            # Data formats
            '.csv', '.tsv', '.json', '.jsonl', '.jsn', '.xml', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg', '.config',
            # Web
            '.html', '.htm', '.css', '.scss', '.sass', '.less',
            # Code files
            '.js', '.jsx', '.ts', '.tsx', '.py', '.pyw', '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
            # Shell & scripts
            '.sh', '.bash', '.zsh', '.bat', '.cmd', '.ps1', '.psm1',
            # Other
            '.sql', '.r', '.m', '.dockerfile', '.env', '.gitignore', '.editorconfig', '.properties', '.gradle'
        },
        'archive': {'.zip', '.gz', '.7z', '.tar', '.tgz', '.tar.gz', '.tar.bz2', '.bz2', '.rar'}
    }
    
    # All supported extensions (flattened)
    ALL_EXTENSIONS = set()
    for ext_list in SUPPORTED_EXTENSIONS.values():
        ALL_EXTENSIONS.update(ext_list)
    
    # -------------------------------------------------------------------------
    # OCR SETTINGS (Tesseract)
    # -------------------------------------------------------------------------
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    OCR_LANGUAGE = 'eng'  # English, can add: 'eng+fra+deu' for multiple
    OCR_CONFIG = '--psm 3'  # Page segmentation mode: Fully automatic
    
    # Image preprocessing for better OCR
    OCR_ENHANCE_IMAGES = True
    OCR_DPI = 300  # Resolution for OCR
    
    # -------------------------------------------------------------------------
    # PDF SETTINGS
    # -------------------------------------------------------------------------
    PDF_EXTRACT_IMAGES = True
    PDF_EXTRACT_TABLES = True
    PDF_PRESERVE_LAYOUT = True
    
    # -------------------------------------------------------------------------
    # ZIP EXTRACTION SETTINGS
    # -------------------------------------------------------------------------
    MAX_ZIP_DEPTH = 10  # Maximum nesting level for ZIP files
    EXTRACT_TEMP_FOLDER = os.path.join(OUTPUT_FOLDER, 'temp_extracted')
    os.makedirs(EXTRACT_TEMP_FOLDER, exist_ok=True)
    
    # -------------------------------------------------------------------------
    # ERROR HANDLING
    # -------------------------------------------------------------------------
    CONTINUE_ON_ERROR = True  # Don't stop on individual file errors
    LOG_ERRORS_TO_FILE = True
    ERROR_LOG_PATH = os.path.join(OUTPUT_FOLDER, 'errors.log')
    
    # -------------------------------------------------------------------------
    # LOGGING SETTINGS
    # -------------------------------------------------------------------------
    DEBUG_MODE = False  # Enable debug mode for detailed logging
    LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_TO_CONSOLE = True
    LOG_TO_FILE = True
    LOG_FILE_PATH = os.path.join(OUTPUT_FOLDER, 'extraction.log')
    
    # Log format
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # -------------------------------------------------------------------------
    # PERFORMANCE SETTINGS
    # -------------------------------------------------------------------------
    # Memory management
    MAX_FILE_SIZE_MB = 500  # Skip files larger than this (safety)
    BATCH_SAVE_INTERVAL = 100  # Save JSON every N files (progress saving)
    
    # Progress update frequency
    PROGRESS_UPDATE_INTERVAL = 0.5  # Seconds between GUI updates
    
    # -------------------------------------------------------------------------
    # METADATA EXTRACTION
    # -------------------------------------------------------------------------
    EXTRACT_FILE_METADATA = True  # Size, dates, permissions
    EXTRACT_DOCUMENT_METADATA = True  # Author, title, keywords
    CALCULATE_CHECKSUMS = True  # MD5 hash for verification
    
    # -------------------------------------------------------------------------
    # ENCODING DETECTION
    # -------------------------------------------------------------------------
    DEFAULT_ENCODING = 'utf-8'
    FALLBACK_ENCODINGS = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    AUTO_DETECT_ENCODING = True
    
    # -------------------------------------------------------------------------
    # GUI SETTINGS
    # -------------------------------------------------------------------------
    WINDOW_TITLE = "Universal Document Extractor"
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    THEME_COLOR = "#2196F3"  # Material Blue
    
    # -------------------------------------------------------------------------
    # VALIDATION
    # -------------------------------------------------------------------------
    VALIDATE_JSON_OUTPUT = True  # Verify JSON is valid before saving
    SKIP_EMPTY_FILES = True  # Don't process 0-byte files
    SKIP_SYSTEM_FILES = True  # Ignore hidden/system files
    
    # System file patterns to skip
    SKIP_PATTERNS = {
        'thumbs.db', 'desktop.ini', '.ds_store',
        '~$*',  # Office temp files
        '__pycache__', '*.pyc'
    }
    
    # -------------------------------------------------------------------------
    # TIMESTAMP FORMAT
    # -------------------------------------------------------------------------
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
    JSON_FILENAME_FORMAT = 'extraction_%Y%m%d_%H%M%S.json'
    
    @staticmethod
    def get_output_filename():
        """Generate timestamped output filename"""
        from datetime import datetime
        return datetime.now().strftime(Config.JSON_FILENAME_FORMAT)
    
    @staticmethod
    def get_full_output_path():
        """Get complete output file path"""
        return os.path.join(Config.OUTPUT_FOLDER, Config.get_output_filename())
    
    @staticmethod
    def validate_tesseract():
        """Check if Tesseract is installed and accessible"""
        import os
        if not os.path.exists(Config.TESSERACT_PATH):
            return False, f"Tesseract not found at {Config.TESSERACT_PATH}"
        return True, "Tesseract OCR found"
    
    @staticmethod
    def get_file_type_category(extension):
        """Get category for file extension"""
        extension = extension.lower()
        for category, extensions in Config.SUPPORTED_EXTENSIONS.items():
            if extension in extensions:
                return category
        return 'unknown'


# ============================================================================
# USAGE EXAMPLE
# ============================================================================
# from config import Config
# 
# output_path = Config.get_full_output_path()
# print(f"Output will be saved to: {output_path}")
# 
# is_valid, message = Config.validate_tesseract()
# print(f"Tesseract check: {message}")
# ============================================================================
