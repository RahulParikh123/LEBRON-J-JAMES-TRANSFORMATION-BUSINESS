"""
CSV file handler
"""
from typing import Dict, Any, List
import pandas as pd
from pathlib import Path
from .base_handler import BaseHandler


class CSVHandler(BaseHandler):
    """Handler for CSV files"""
    
    def can_handle(self, file_path: str) -> bool:
        """Check if file is a CSV file"""
        ext = Path(file_path).suffix.lower()
        return ext in ['.csv', '.tsv']
    
    def get_supported_extensions(self) -> List[str]:
        return ['.csv', '.tsv']
    
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        """Extract data from CSV file"""
        metadata = self.extract_metadata(source)
        
        # Auto-detect delimiter
        delimiter = kwargs.get('delimiter', None)
        if delimiter is None:
            delimiter = ',' if source.endswith('.csv') else '\t'
        
        try:
            # Read CSV with error handling
            df = pd.read_csv(
                source,
                delimiter=delimiter,
                encoding=kwargs.get('encoding', 'utf-8'),
                on_bad_lines='skip',
                **{k: v for k, v in kwargs.items() if k not in ['delimiter', 'encoding']}
            )
            
            df = self.normalize_dataframe(df)
            records = df.to_dict('records')
            
            # Generate text representation
            text_content = self._dataframe_to_text(df)
            
            metadata.update({
                'row_count': len(df),
                'column_count': len(df.columns),
                'delimiter': delimiter
            })
            
            return {
                'data': records,
                'metadata': metadata,
                'text_content': [text_content],
                'structure': {
                    'columns': list(df.columns),
                    'format': 'csv',
                    'delimiter': delimiter
                }
            }
            
        except Exception as e:
            raise ValueError(f"Error reading CSV file {source}: {str(e)}")
    
    def _dataframe_to_text(self, df: pd.DataFrame) -> str:
        """Convert DataFrame to text representation"""
        lines = [f"CSV Data with {len(df)} rows and {len(df.columns)} columns"]
        lines.append(f"Columns: {', '.join(df.columns)}")
        lines.append("")
        
        # Include sample rows
        sample_size = min(10, len(df))
        for idx, row in df.head(sample_size).iterrows():
            row_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
            lines.append(f"Row {idx}: {row_text}")
        
        return "\n".join(lines)

