"""
Excel file handler (.xlsx, .xls)
"""
from typing import Dict, Any, List
import pandas as pd
from pathlib import Path
from .base_handler import BaseHandler


class ExcelHandler(BaseHandler):
    """Handler for Excel files"""
    
    def can_handle(self, file_path: str) -> bool:
        """Check if file is an Excel file"""
        ext = Path(file_path).suffix.lower()
        return ext in ['.xlsx', '.xls', '.xlsm']
    
    def get_supported_extensions(self) -> List[str]:
        return ['.xlsx', '.xls', '.xlsm']
    
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        """
        Extract data from Excel file
        
        Supports multiple sheets and preserves structure
        """
        metadata = self.extract_metadata(source)
        result = {
            'data': [],
            'metadata': metadata,
            'text_content': [],
            'structure': {}
        }
        
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(source, engine='openpyxl')
            sheets_data = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name, **kwargs)
                
                # Handle empty dataframes
                if df.empty:
                    sheets_data[sheet_name] = {
                        'data': [],
                        'columns': [],
                        'row_count': 0
                    }
                    continue
                
                df = self.normalize_dataframe(df)
                
                # Convert to records for JSON serialization (all values are now strings)
                records = df.to_dict('records')
                sheets_data[sheet_name] = {
                    'data': records,
                    'columns': list(df.columns),
                    'row_count': len(df)
                }
                
                # Generate text representation for LLM training
                text_repr = self._dataframe_to_text(df, sheet_name)
                result['text_content'].append(text_repr)
            
            result['data'] = sheets_data
            result['structure'] = {
                'sheet_count': len(excel_file.sheet_names),
                'sheet_names': excel_file.sheet_names,
                'format': 'excel'
            }
            
            metadata.update({
                'sheet_count': len(excel_file.sheet_names),
                'total_rows': sum(s['row_count'] for s in sheets_data.values())
            })
            
        except Exception as e:
            raise ValueError(f"Error reading Excel file {source}: {str(e)}")
        
        return result
    
    def _dataframe_to_text(self, df: pd.DataFrame, sheet_name: str) -> str:
        """Convert DataFrame to text representation for LLM training"""
        lines = [f"Sheet: {sheet_name}"]
        lines.append(f"Columns: {', '.join(df.columns)}")
        lines.append("")
        
        # Include sample rows (first 10 rows for context)
        sample_size = min(10, len(df))
        for idx, row in df.head(sample_size).iterrows():
            # Convert all values to strings to avoid type errors
            row_text = " | ".join([f"{col}: {str(val) if pd.notna(val) else ''}" for col, val in row.items()])
            lines.append(f"Row {idx}: {row_text}")
        
        return "\n".join(lines)

