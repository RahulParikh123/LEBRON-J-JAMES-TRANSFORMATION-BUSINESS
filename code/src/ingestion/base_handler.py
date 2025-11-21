"""
Base handler interface for all format handlers
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pathlib import Path
import pandas as pd


class BaseHandler(ABC):
    """Abstract base class for all data format handlers"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.metadata = {}
    
    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        """Check if this handler can process the given file"""
        pass
    
    @abstractmethod
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        """
        Extract data from source
        
        Returns:
            Dict with keys:
                - 'data': List of records or DataFrame
                - 'metadata': Dict with file metadata
                - 'text_content': Optional text content for LLM training
                - 'structure': Optional structural information
        """
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """Return list of supported file extensions"""
        pass
    
    def normalize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize DataFrame: standardize column names, types, etc."""
        # Standardize column names (convert to string first to avoid type errors)
        # Handle case where column names might be floats, ints, or other types
        new_columns = []
        for col in df.columns:
            # Convert to string first, then normalize
            col_str = str(col) if pd.notna(col) else f"column_{len(new_columns)}"
            col_str = col_str.strip().lower().replace(' ', '_')
            new_columns.append(col_str)
        df.columns = new_columns
        
        # Convert ALL columns to string to avoid type mixing issues
        for col in df.columns:
            # Replace NaN with empty string, then convert to string
            df[col] = df[col].fillna('').astype(str)
        
        return df
    
    def extract_metadata(self, source: str) -> Dict[str, Any]:
        """Extract basic metadata about the source"""
        path = Path(source)
        return {
            'source_path': str(path),
            'file_name': path.name,
            'file_size': path.stat().st_size if path.exists() else 0,
            'handler_type': self.__class__.__name__,
        }

