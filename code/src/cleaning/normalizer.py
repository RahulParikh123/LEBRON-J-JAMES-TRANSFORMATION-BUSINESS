"""
Data normalization module
"""
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import re


class DataNormalizer:
    """Normalize data structure, types, and formats"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.normalization_stats = {}
    
    def normalize(self, data: Any, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Normalize data based on its structure
        
        Returns normalized data with statistics
        """
        if isinstance(data, pd.DataFrame):
            return self._normalize_dataframe(data, metadata)
        elif isinstance(data, list):
            return self._normalize_list(data, metadata)
        elif isinstance(data, dict):
            return self._normalize_dict(data, metadata)
        else:
            return {'data': data, 'stats': {}}
    
    def _normalize_dataframe(self, df: pd.DataFrame, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Normalize a pandas DataFrame"""
        original_shape = df.shape
        df = df.copy()
        
        stats = {
            'original_rows': original_shape[0],
            'original_columns': original_shape[1],
            'transformations': []
        }
        
        # 1. Standardize column names
        original_columns = df.columns.tolist()
        df.columns = self._normalize_column_names(df.columns)
        if list(df.columns) != original_columns:
            stats['transformations'].append('column_names_normalized')
        
        # 2. Remove completely empty rows and columns
        df = df.dropna(how='all').dropna(axis=1, how='all')
        if df.shape != original_shape:
            stats['transformations'].append('empty_rows_columns_removed')
        
        # 3. Normalize data types
        df = self._normalize_types(df)
        stats['transformations'].append('types_normalized')
        
        # 4. Normalize string values
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            df[col] = df[col].apply(self._normalize_string)
        
        # 5. Handle missing values
        df = self._normalize_missing_values(df)
        
        stats['final_rows'] = df.shape[0]
        stats['final_columns'] = df.shape[1]
        stats['columns_normalized'] = list(df.columns)
        
        return {
            'data': df,
            'stats': stats
        }
    
    def _normalize_list(self, data: List, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Normalize a list of records"""
        if not data:
            return {'data': [], 'stats': {}}
        
        # Convert to DataFrame if possible
        try:
            df = pd.DataFrame(data)
            return self._normalize_dataframe(df, metadata)
        except:
            # If conversion fails, normalize each item
            normalized = [self._normalize_item(item) for item in data]
            return {'data': normalized, 'stats': {'items_normalized': len(normalized)}}
    
    def _normalize_dict(self, data: Dict, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Normalize a dictionary"""
        normalized = {}
        for key, value in data.items():
            norm_key = self._normalize_string(str(key))
            normalized[norm_key] = self._normalize_item(value)
        
        return {'data': normalized, 'stats': {}}
    
    def _normalize_item(self, item: Any) -> Any:
        """Normalize a single item"""
        if isinstance(item, str):
            return self._normalize_string(item)
        elif isinstance(item, (dict, list)):
            return self.normalize(item)['data']
        else:
            return item
    
    def _normalize_column_names(self, columns: pd.Index) -> pd.Index:
        """Normalize column names"""
        normalized = []
        for col in columns:
            # Convert to string, lowercase, replace spaces/special chars
            col_str = str(col)
            col_str = col_str.strip().lower()
            col_str = re.sub(r'[^\w\s]', '_', col_str)
            col_str = re.sub(r'\s+', '_', col_str)
            col_str = re.sub(r'_+', '_', col_str)
            col_str = col_str.strip('_')
            
            # Ensure it's a valid identifier
            if not col_str or col_str[0].isdigit():
                col_str = 'col_' + col_str
            
            normalized.append(col_str)
        
        # Handle duplicates
        seen = {}
        result = []
        for col in normalized:
            if col in seen:
                seen[col] += 1
                result.append(f"{col}_{seen[col]}")
            else:
                seen[col] = 0
                result.append(col)
        
        return pd.Index(result)
    
    def _normalize_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize data types intelligently"""
        df = df.copy()
        
        for col in df.columns:
            # Try to infer and convert types
            if df[col].dtype == 'object':
                # Try numeric conversion
                numeric = pd.to_numeric(df[col], errors='coerce')
                if not numeric.isna().all():
                    df[col] = numeric
                    continue
                
                # Try datetime conversion
                datetime_col = pd.to_datetime(df[col], errors='coerce')
                if not datetime_col.isna().all():
                    df[col] = datetime_col
                    continue
                
                # Keep as string but normalize
                df[col] = df[col].astype(str)
        
        return df
    
    def _normalize_string(self, value: Any) -> str:
        """Normalize string values"""
        if pd.isna(value) or value is None:
            return ''
        
        value = str(value)
        
        # Remove leading/trailing whitespace
        value = value.strip()
        
        # Normalize whitespace
        value = re.sub(r'\s+', ' ', value)
        
        # Remove control characters
        value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
        
        return value
    
    def _normalize_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize missing values"""
        df = df.copy()
        
        # Replace various representations of missing values
        missing_indicators = ['', 'null', 'none', 'n/a', 'na', 'nan', 'nil', '?', '-']
        
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].replace(missing_indicators, np.nan)
        
        return df

