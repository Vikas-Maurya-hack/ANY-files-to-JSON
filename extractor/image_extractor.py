# ============================================================================
# IMAGE EXTRACTOR - OCR text extraction from images
# ============================================================================

from .base_extractor import BaseExtractor
from typing import Dict, Any
from pathlib import Path
import logging

class ImageExtractor(BaseExtractor):
    """Extract text from images using OCR"""
    
    def extract(self) -> Dict[str, Any]:
        """
        Extract text from image using Tesseract OCR
        
        Returns:
            Dictionary with OCR text and image metadata
        """
        try:
            import pytesseract
            from PIL import Image
            import cv2
            import numpy as np
            from config import Config
            
            # Check if Tesseract is installed first
            tesseract_path = Path(Config.TESSERACT_PATH)
            if not tesseract_path.exists():
                # Return graceful skip instead of error
                return self.create_result_dict(
                    content={
                        'text': '',
                        'note': 'Tesseract OCR not installed - image skipped',
                        'image_metadata': self._get_basic_metadata()
                    },
                    status='skipped',
                    error_message='Tesseract OCR not installed'
                )
            
            # Set Tesseract path
            pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH
            
            # Load image
            image = Image.open(self.file_path)
            
            # Get image metadata
            image_metadata = {
                'format': image.format,
                'mode': image.mode,
                'size': image.size,  # (width, height)
                'width': image.width,
                'height': image.height,
            }
            
            # Enhance image if configured
            if Config.OCR_ENHANCE_IMAGES:
                # Convert PIL to OpenCV format
                img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Preprocess for better OCR
                img_cv = self._preprocess_image(img_cv)
                
                # Convert back to PIL
                image = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
            
            # Perform OCR
            text = pytesseract.image_to_string(
                image,
                lang=Config.OCR_LANGUAGE,
                config=Config.OCR_CONFIG
            )
            
            # Get OCR confidence data
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(conf) for conf in ocr_data['conf'] if conf != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            content = {
                'text': text.strip(),
                'image_metadata': image_metadata,
                'ocr_confidence': round(avg_confidence, 2),
                'extraction_method': 'tesseract_ocr'
            }
            
            return self.create_result_dict(content)
            
        except ImportError as e:
            error_msg = f"Missing dependency for OCR: {e}. Install: pip install pytesseract pillow opencv-python"
            self.logger.error(error_msg)
            return self.create_result_dict(
                content={'error': error_msg},
                status='error',
                error_message=error_msg
            )
        except Exception as e:
            self.logger.error(f"Image OCR failed: {e}")
            return self.create_result_dict(
                content={'error': str(e)},
                status='error',
                error_message=str(e)
            )
    
    def _preprocess_image(self, img):
        """
        Preprocess image for better OCR results
        
        Args:
            img: OpenCV image
            
        Returns:
            Preprocessed image
        """
        import cv2
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(binary, None, 10, 7, 21)
        
        return cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)
    
    def _get_basic_metadata(self) -> Dict:
        """Get basic image metadata without OCR"""
        try:
            from PIL import Image
            image = Image.open(self.file_path)
            return {
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'width': image.width,
                'height': image.height,
            }
        except:
            return {}
