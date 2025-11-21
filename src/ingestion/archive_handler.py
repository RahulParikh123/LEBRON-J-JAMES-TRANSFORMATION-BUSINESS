"""
Archive file handler (.zip, .tar, .gz, .rar, .7z)
"""
from typing import Dict, Any, List
from pathlib import Path
import zipfile
import tarfile
from .base_handler import BaseHandler


class ArchiveHandler(BaseHandler):
    """Handler for archive files"""
    
    def can_handle(self, file_path: str) -> bool:
        """Check if file is an archive"""
        ext = Path(file_path).suffix.lower()
        return ext in ['.zip', '.tar', '.gz', '.rar', '.7z']
    
    def get_supported_extensions(self) -> List[str]:
        return ['.zip', '.tar', '.gz', '.rar', '.7z']
    
    def extract(self, source: str, extract_files: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Extract data from archive file
        
        Args:
            extract_files: If True, extracts and processes files in archive
        """
        metadata = self.extract_metadata(source)
        result = {
            'data': [],
            'metadata': metadata,
            'text_content': [],
            'structure': {}
        }
        
        try:
            ext = Path(source).suffix.lower()
            file_list = []
            
            if ext == '.zip':
                with zipfile.ZipFile(source, 'r') as zip_ref:
                    file_list = zip_ref.namelist()
                    result['structure'] = {
                        'format': 'zip',
                        'file_count': len(file_list),
                        'files': file_list[:100]  # Limit to first 100
                    }
            
            elif ext in ['.tar', '.gz']:
                mode = 'r:gz' if ext == '.gz' else 'r'
                with tarfile.open(source, mode) as tar_ref:
                    file_list = [member.name for member in tar_ref.getmembers() if member.isfile()]
                    result['structure'] = {
                        'format': 'tar' if ext == '.tar' else 'gzip',
                        'file_count': len(file_list),
                        'files': file_list[:100]
                    }
            
            else:
                # RAR and 7z require additional libraries
                result['structure'] = {
                    'format': ext[1:],
                    'note': f'{ext} extraction requires additional libraries (rarfile, py7zr)'
                }
                file_list = []
            
            result['data'] = [{'files': file_list}]
            result['text_content'] = [f"Archive: {Path(source).name}\nFiles: {len(file_list)}"]
            
            metadata.update({
                'file_count': len(file_list),
                'archive_type': ext[1:]
            })
            
        except Exception as e:
            raise ValueError(f"Error reading archive file {source}: {str(e)}")
        
        return result

