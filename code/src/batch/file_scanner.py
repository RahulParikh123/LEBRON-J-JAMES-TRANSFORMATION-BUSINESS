"""
File scanner for discovering files in directories
"""
from typing import List, Dict, Any, Optional
from pathlib import Path
import fnmatch
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FileInfo:
    """Information about a discovered file"""
    path: Path
    name: str
    extension: str
    size: int
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    file_type: Optional[str] = None


class FileScanner:
    """Scan directories for files matching patterns"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.default_patterns = [
            '*.xlsx', '*.xls', '*.xlsm',  # Excel
            '*.csv', '*.tsv',              # CSV
            '*.json',                       # JSON
            '*.pptx', '*.ppt',             # PowerPoint
            '*.docx', '*.doc',             # Word
        ]
    
    def scan_directory(
        self,
        directory: str,
        patterns: Optional[List[str]] = None,
        recursive: bool = True
    ) -> List[FileInfo]:
        """
        Scan directory for files matching patterns
        
        Args:
            directory: Directory path to scan
            patterns: File patterns to match (default: all supported)
            recursive: Whether to scan subdirectories
        
        Returns:
            List of FileInfo objects
        """
        directory_path = Path(directory)
        if not directory_path.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        
        if not directory_path.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")
        
        patterns = patterns or self.default_patterns
        files = []
        
        if recursive:
            search_path = directory_path.rglob('*')
        else:
            search_path = directory_path.glob('*')
        
        for path in search_path:
            if path.is_file():
                # Check if file matches any pattern
                if any(fnmatch.fnmatch(path.name.lower(), p.lower()) for p in patterns):
                    try:
                        stat = path.stat()
                        file_info = FileInfo(
                            path=path,
                            name=path.name,
                            extension=path.suffix.lower(),
                            size=stat.st_size,
                            created_at=datetime.fromtimestamp(stat.st_ctime),
                            modified_at=datetime.fromtimestamp(stat.st_mtime),
                            file_type=self._detect_file_type(path.suffix)
                        )
                        files.append(file_info)
                    except (OSError, PermissionError):
                        # Skip files we can't access
                        continue
        
        return sorted(files, key=lambda f: f.path)
    
    def _detect_file_type(self, extension: str) -> str:
        """Detect file type from extension"""
        extension = extension.lower()
        type_map = {
            '.xlsx': 'excel',
            '.xls': 'excel',
            '.xlsm': 'excel',
            '.csv': 'csv',
            '.tsv': 'csv',
            '.json': 'json',
            '.pptx': 'powerpoint',
            '.ppt': 'powerpoint',
            '.docx': 'word',
            '.doc': 'word',
        }
        return type_map.get(extension, 'unknown')
    
    def get_file_summary(self, files: List[FileInfo]) -> Dict[str, Any]:
        """Get summary statistics about scanned files"""
        if not files:
            return {
                'total_files': 0,
                'total_size': 0,
                'by_type': {},
                'by_extension': {}
            }
        
        total_size = sum(f.size for f in files)
        by_type = {}
        by_extension = {}
        
        for file in files:
            by_type[file.file_type] = by_type.get(file.file_type, 0) + 1
            by_extension[file.extension] = by_extension.get(file.extension, 0) + 1
        
        return {
            'total_files': len(files),
            'total_size': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'total_size_gb': round(total_size / (1024 * 1024 * 1024), 2),
            'by_type': by_type,
            'by_extension': by_extension
        }

