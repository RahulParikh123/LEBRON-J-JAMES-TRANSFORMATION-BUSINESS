"""
Data deduplication module
"""
from typing import Any, Dict, List, Optional, Set
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from recordlinkage import Compare


class DataDeduplicator:
    """Remove duplicate records from data"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.similarity_threshold = self.config.get('similarity_threshold', 0.85)
        self.exact_match_only = self.config.get('exact_match_only', False)
    
    def deduplicate(self, data: Any, key_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Remove duplicates from data
        
        Args:
            data: DataFrame, list of dicts, or dict
            key_columns: Columns to use for duplicate detection (if None, uses all)
        
        Returns:
            Dict with deduplicated data and statistics
        """
        if isinstance(data, pd.DataFrame):
            return self._deduplicate_dataframe(data, key_columns)
        elif isinstance(data, list):
            return self._deduplicate_list(data, key_columns)
        else:
            return {'data': data, 'stats': {'duplicates_removed': 0}}
    
    def _deduplicate_dataframe(self, df: pd.DataFrame, key_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Remove duplicates from DataFrame"""
        original_count = len(df)
        df = df.copy()
        
        stats = {
            'original_count': original_count,
            'exact_duplicates_removed': 0,
            'fuzzy_duplicates_removed': 0,
            'final_count': 0
        }
        
        # 1. Remove exact duplicates
        if key_columns:
            # Use specific columns for duplicate detection
            df_unique = df.drop_duplicates(subset=key_columns, keep='first')
        else:
            # Use all columns
            df_unique = df.drop_duplicates(keep='first')
        
        exact_dups = original_count - len(df_unique)
        stats['exact_duplicates_removed'] = exact_dups
        
        # 2. Remove fuzzy duplicates if enabled
        if not self.exact_match_only and len(df_unique) > 1:
            df_unique, fuzzy_dups = self._remove_fuzzy_duplicates(df_unique, key_columns)
            stats['fuzzy_duplicates_removed'] = fuzzy_dups
        
        stats['final_count'] = len(df_unique)
        stats['total_duplicates_removed'] = original_count - len(df_unique)
        
        return {
            'data': df_unique,
            'stats': stats
        }
    
    def _deduplicate_list(self, data: List[Dict], key_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Remove duplicates from list of dictionaries"""
        if not data:
            return {'data': [], 'stats': {'duplicates_removed': 0}}
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        result = self._deduplicate_dataframe(df, key_columns)
        
        # Convert back to list of dicts
        result['data'] = result['data'].to_dict('records')
        
        return result
    
    def _remove_fuzzy_duplicates(self, df: pd.DataFrame, key_columns: Optional[List[str]] = None) -> tuple:
        """
        Remove fuzzy duplicates using similarity matching
        
        Returns: (deduplicated_df, count_removed)
        """
        if len(df) <= 1:
            return df, 0
        
        # Select columns for comparison
        if key_columns:
            compare_cols = [col for col in key_columns if col in df.columns]
        else:
            # Use string columns for comparison
            compare_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not compare_cols:
            return df, 0
        
        # Create a signature for each row
        df['_signature'] = df[compare_cols].apply(
            lambda row: ' '.join(str(val) for val in row if pd.notna(val)), axis=1
        )
        
        # Find similar rows
        indices_to_remove = set()
        
        for i in range(len(df)):
            if i in indices_to_remove:
                continue
            
            sig1 = df.iloc[i]['_signature']
            
            for j in range(i + 1, len(df)):
                if j in indices_to_remove:
                    continue
                
                sig2 = df.iloc[j]['_signature']
                
                # Calculate similarity
                similarity = fuzz.ratio(sig1.lower(), sig2.lower()) / 100.0
                
                if similarity >= self.similarity_threshold:
                    indices_to_remove.add(j)
        
        # Remove duplicates
        df_clean = df.drop(index=df.index[list(indices_to_remove)])
        df_clean = df_clean.drop(columns=['_signature'])
        
        return df_clean, len(indices_to_remove)
    
    def find_duplicate_groups(self, df: pd.DataFrame, key_columns: Optional[List[str]] = None) -> List[List[int]]:
        """
        Find groups of duplicate records
        
        Returns list of groups, where each group contains indices of duplicate records
        """
        groups = []
        processed = set()
        
        if key_columns:
            compare_cols = [col for col in key_columns if col in df.columns]
        else:
            compare_cols = df.columns.tolist()
        
        for i in range(len(df)):
            if i in processed:
                continue
            
            group = [i]
            row1 = df.iloc[i]
            
            for j in range(i + 1, len(df)):
                if j in processed:
                    continue
                
                row2 = df.iloc[j]
                
                # Check if rows are similar
                if self._rows_similar(row1, row2, compare_cols):
                    group.append(j)
                    processed.add(j)
            
            if len(group) > 1:
                groups.append(group)
                processed.add(i)
        
        return groups
    
    def _rows_similar(self, row1: pd.Series, row2: pd.Series, columns: List[str]) -> bool:
        """Check if two rows are similar"""
        if self.exact_match_only:
            return row1[columns].equals(row2[columns])
        
        # Fuzzy matching
        sig1 = ' '.join(str(row1[col]) for col in columns if pd.notna(row1[col]))
        sig2 = ' '.join(str(row2[col]) for col in columns if pd.notna(row2[col]))
        
        similarity = fuzz.ratio(sig1.lower(), sig2.lower()) / 100.0
        return similarity >= self.similarity_threshold

