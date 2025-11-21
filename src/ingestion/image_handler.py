"""
Image file handler (.png, .jpg, .jpeg, .gif, .bmp, .tiff, .webp)
"""
from typing import Dict, Any, List
from pathlib import Path
from .base_handler import BaseHandler

try:
    from PIL import Image, ExifTags
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class ImageHandler(BaseHandler):
    """Handler for image files"""
    
    def can_handle(self, file_path: str) -> bool:
        """Check if file is an image"""
        ext = Path(file_path).suffix.lower()
        return ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg']
    
    def get_supported_extensions(self) -> List[str]:
        return ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp', '.svg']
    
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        """Extract data from image file"""
        metadata = self.extract_metadata(source)
        result = {
            'data': [],
            'metadata': metadata,
            'text_content': [],
            'structure': {}
        }
        
        try:
            image_info = {}
            text_content = []
            
            if PIL_AVAILABLE:
                with Image.open(source) as img:
                    image_info = {
                        'format': img.format,
                        'mode': img.mode,
                        'size': img.size,
                        'width': img.width,
                        'height': img.height
                    }
                    
                    # Extract EXIF data
                    exif_data = {}
                    if hasattr(img, '_getexif') and img._getexif():
                        for tag, value in img._getexif().items():
                            decoded = ExifTags.TAGS.get(tag, tag)
                            exif_data[decoded] = str(value)
                    
                    if exif_data:
                        image_info['exif'] = exif_data
                    
                    text_content.append(f"Image: {Path(source).name}")
                    text_content.append(f"Format: {img.format}")
                    text_content.append(f"Size: {img.width}x{img.height}")
                    text_content.append(f"Mode: {img.mode}")
                    
                    # OCR if available
                    if OCR_AVAILABLE:
                        try:
                            ocr_text = pytesseract.image_to_string(img)
                            if ocr_text.strip():
                                text_content.append(f"\nExtracted Text:\n{ocr_text}")
                                image_info['ocr_text'] = ocr_text
                        except Exception:
                            pass  # OCR failed, continue without it
            
            else:
                # Basic info without PIL
                image_info = {
                    'file_path': source,
                    'note': 'PIL not available for detailed image analysis'
                }
                text_content.append(f"Image file: {Path(source).name}")
            
            result['data'] = [image_info]
            result['text_content'] = text_content
            result['structure'] = {
                'format': 'image',
                'image_info': image_info
            }
            
            metadata.update(image_info)
            
        except Exception as e:
            raise ValueError(f"Error reading image file {source}: {str(e)}")
        
        return result

