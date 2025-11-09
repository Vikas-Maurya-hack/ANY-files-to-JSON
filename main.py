# ============================================================================
# MAIN - Application entry point and orchestration
# ============================================================================

import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from datetime import datetime
from typing import List, Optional
import queue

from config import Config
from utils.logger import setup_logger
from utils.progress import ProgressTracker
from utils.file_scanner import FileScanner
from extractor import (
    PDFExtractor, ImageExtractor, DOCXExtractor,
    MarkdownExtractor, ZIPExtractor, TextExtractor,
    GZIPExtractor, SevenZipExtractor, TARExtractor, RARExtractor
)

# Setup logger
logger = setup_logger()


def get_extractor(file_path: Path):
    """Get appropriate extractor for file type"""
    ext = file_path.suffix.lower()
    file_path_lower = str(file_path).lower()
    
    # Check for .tar.gz and .tgz first
    if file_path_lower.endswith(('.tar.gz', '.tgz')):
        return GZIPExtractor(file_path)
    elif ext == '.pdf':
        return PDFExtractor(file_path)
    elif ext in Config.SUPPORTED_EXTENSIONS['images']:
        return ImageExtractor(file_path)
    elif ext in ['.docx', '.doc']:
        return DOCXExtractor(file_path)
    elif ext in Config.SUPPORTED_EXTENSIONS['markdown']:
        return MarkdownExtractor(file_path)
    elif ext == '.zip':
        return ZIPExtractor(file_path)
    elif ext == '.gz':
        return GZIPExtractor(file_path)
    elif ext == '.7z':
        return SevenZipExtractor(file_path)
    elif ext == '.tar':
        return TARExtractor(file_path)
    elif ext == '.rar':
        return RARExtractor(file_path)
    elif ext in Config.SUPPORTED_EXTENSIONS['text']:
        return TextExtractor(file_path)
    else:
        return None


def extract_single_file(file_path: Path, progress: ProgressTracker, msg_queue: Optional[queue.Queue] = None) -> dict:
    """Extract content from a single file"""
    try:
        # Get extractor
        extractor = get_extractor(file_path)
        
        if not extractor:
            logger.warning(f"No extractor for {file_path}")
            progress.update(skipped=True, filename=str(file_path))
            if msg_queue:
                msg_queue.put(('log', f"Skipped: {file_path.name} (unsupported type)", "WARNING"))
            return None
        
        # Extract content
        result = extractor.safe_extract()
        
        # Update progress
        success = result.get('extraction_status') == 'success'
        progress.update(success=success, filename=str(file_path))
        
        # Send progress update to GUI
        if msg_queue:
            stats = progress.get_stats()
            msg_queue.put(('progress', stats))
            
            if not success:
                msg_queue.put(('log', f"Error: {file_path.name} - {result.get('error_message')}", "ERROR"))
        
        return result
    
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        progress.update(success=False, filename=str(file_path))
        
        if msg_queue:
            msg_queue.put(('log', f"Error: {file_path.name} - {str(e)}", "ERROR"))
        
        return None


def extract_documents(source, msg_queue: Optional[queue.Queue] = None) -> Path:
    """
    Main extraction function
    
    Args:
        source: Either a Path to directory or a List[Path] of specific files
        msg_queue: Queue for GUI updates
        
    Returns:
        Path to output JSON file
    """
    # Determine if we're processing a directory or file list
    if isinstance(source, list):
        # File list mode
        files = source
        source_dir = files[0].parent if files else Path.cwd()
        logger.info(f"Starting extraction from {len(files)} selected files")
        
        if msg_queue:
            msg_queue.put(('log', f"Processing {len(files)} selected files...", "INFO"))
    else:
        # Directory mode
        source_dir = source
        logger.info(f"Starting extraction from: {source_dir}")
        
        if msg_queue:
            msg_queue.put(('log', f"Scanning {source_dir}...", "INFO"))
        
        # Scan for files
        scanner = FileScanner()
        files = scanner.scan_directory(source_dir)
        
        if not files:
            logger.warning("No supported files found!")
            if msg_queue:
                msg_queue.put(('log', "No supported files found!", "WARNING"))
            return None
    
    logger.info(f"Found {len(files)} files to process")
    
    # Calculate total size
    scanner = FileScanner()
    stats = scanner.get_file_stats(files)
    
    if msg_queue:
        msg_queue.put(('log', f"Found {len(files)} files ({stats['total_size_human']})", "SUCCESS"))
    
    # Initialize progress tracker
    progress = ProgressTracker(len(files))
    
    # Process files with thread pool
    results = []
    
    with ThreadPoolExecutor(max_workers=Config.MAX_THREADS) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(extract_single_file, file_path, progress, msg_queue): file_path
            for file_path in files
        }
        
        # Process completed tasks
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                logger.error(f"Error in future for {file_path}: {e}")
    
    # Save results to JSON
    output_file = save_results(results, source_dir)
    
    # Final stats
    final_stats = progress.get_stats()
    logger.info(f"Extraction complete! Processed: {final_stats['processed']}, "
                f"Success: {final_stats['successful']}, Failed: {final_stats['failed']}")
    
    if msg_queue:
        msg_queue.put(('complete', output_file))
    
    return output_file


def save_results(results: List[dict], source_dir: Path) -> Path:
    """Save extraction results to JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(Config.OUTPUT_FOLDER) / f"extraction_{timestamp}.json"
    
    # Create comprehensive output
    output_data = {
        'metadata': {
            'extraction_date': datetime.now().isoformat(),
            'source_directory': str(source_dir),
            'total_files': len(results),
            'version': '1.0.0'
        },
        'results': results
    }
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Results saved to: {output_file}")
    return output_file


def main():
    """Main entry point"""
    # Validate Tesseract installation
    if not Config.validate_tesseract():
        logger.warning("Tesseract OCR not found. Image extraction will fail!")
        logger.warning(f"Please install Tesseract and update TESSERACT_PATH in config.py")
    
    # Check if running in GUI or CLI mode
    if len(sys.argv) > 1:
        # CLI mode
        source_dir = Path(sys.argv[1])
        
        if not source_dir.exists():
            logger.error(f"Directory not found: {source_dir}")
            sys.exit(1)
        
        extract_documents(source_dir)
    
    else:
        # GUI mode
        from gui.main_window import MainWindow
        
        logger.info("Starting GUI...")
        app = MainWindow()
        app.run()


if __name__ == '__main__':
    main()
