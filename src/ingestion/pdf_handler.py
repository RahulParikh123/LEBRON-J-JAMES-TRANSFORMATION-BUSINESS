"""
PDF file handler (.pdf)
"""
from typing import Dict, Any, List
from pathlib import Path
from .base_handler import BaseHandler

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    try:
        import pdfplumber
        PDFPLUMBER_AVAILABLE = True
        PDF_AVAILABLE = False
    except ImportError:
        PDF_AVAILABLE = False
        PDFPLUMBER_AVAILABLE = False


class PDFHandler(BaseHandler):
    """Handler for PDF files"""
    
    def can_handle(self, file_path: str) -> bool:
        """Check if file is a PDF"""
        ext = Path(file_path).suffix.lower()
        return ext == '.pdf'
    
    def get_supported_extensions(self) -> List[str]:
        return ['.pdf']
    
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        """Extract data from PDF file"""
        metadata = self.extract_metadata(source)
        result = {
            'data': [],
            'metadata': metadata,
            'text_content': [],
            'structure': {}
        }
        
        try:
            text_content = []
            pages_data = []
            
            if PDFPLUMBER_AVAILABLE:
                # Use pdfplumber for better table extraction
                import pdfplumber
                with pdfplumber.open(source) as pdf:
                    for page_num, page in enumerate(pdf.pages, 1):
                        page_text = page.extract_text() or ""
                        text_content.append(f"Page {page_num}:\n{page_text}")
                        
                        # Extract tables
                        tables = page.extract_tables()
                        for table_num, table in enumerate(tables):
                            if table:
                                pages_data.append({
                                    'page': page_num,
                                    'table': table_num,
                                    'data': table
                                })
            
            elif PDF_AVAILABLE:
                # Fallback to PyPDF2
                with open(source, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page_num, page in enumerate(pdf_reader.pages, 1):
                        page_text = page.extract_text() or ""
                        text_content.append(f"Page {page_num}:\n{page_text}")
            
            else:
                raise ImportError("No PDF library available. Install PyPDF2 or pdfplumber")
            
            result['text_content'] = text_content
            result['data'] = pages_data if pages_data else [{'text': '\n'.join(text_content)}]
            result['structure'] = {
                'format': 'pdf',
                'page_count': len(text_content),
                'has_tables': len(pages_data) > 0
            }
            
            metadata.update({
                'page_count': len(text_content),
                'table_count': len(pages_data)
            })
            
        except Exception as e:
            raise ValueError(f"Error reading PDF file {source}: {str(e)}")
        
        return result

