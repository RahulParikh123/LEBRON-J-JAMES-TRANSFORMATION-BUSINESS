"""
Data formatter - structure data for optimal processing
"""
from typing import Any, Dict, List, Optional
import pandas as pd
import json


class DataFormatter:
    """Format data into structured representations"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    def format(self, data: Any, format_type: str = 'jsonl', 
               include_metadata: bool = True) -> Dict[str, Any]:
        """
        Format data into specified format
        
        Args:
            data: Data to format
            format_type: 'jsonl', 'parquet', 'csv', 'json'
            include_metadata: Whether to include metadata
        
        Returns:
            Formatted data and metadata
        """
        if format_type == 'jsonl':
            return self._format_jsonl(data, include_metadata)
        elif format_type == 'parquet':
            return self._format_parquet(data, include_metadata)
        elif format_type == 'csv':
            return self._format_csv(data, include_metadata)
        elif format_type == 'json':
            return self._format_json(data, include_metadata)
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
    
    def _format_jsonl(self, data: Any, include_metadata: bool) -> Dict[str, Any]:
        """Format as JSONL (JSON Lines)"""
        if isinstance(data, pd.DataFrame):
            records = data.to_dict('records')
        elif isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = [data]
        else:
            records = [{'value': data}]
        
        # Convert to JSONL format
        jsonl_lines = [json.dumps(record, default=str) for record in records]
        jsonl_content = '\n'.join(jsonl_lines)
        
        result = {
            'format': 'jsonl',
            'content': jsonl_content,
            'record_count': len(records)
        }
        
        if include_metadata:
            result['metadata'] = {
                'format': 'jsonl',
                'encoding': 'utf-8',
                'line_count': len(jsonl_lines)
            }
        
        return result
    
    def _format_parquet(self, data: Any, include_metadata: bool) -> Dict[str, Any]:
        """Format as Parquet"""
        if not isinstance(data, pd.DataFrame):
            if isinstance(data, list):
                data = pd.DataFrame(data)
            else:
                data = pd.DataFrame([{'value': data}])
        
        result = {
            'format': 'parquet',
            'data': data,
            'record_count': len(data)
        }
        
        if include_metadata:
            result['metadata'] = {
                'format': 'parquet',
                'columns': list(data.columns),
                'row_count': len(data),
                'column_types': {col: str(data[col].dtype) for col in data.columns}
            }
        
        return result
    
    def _format_csv(self, data: Any, include_metadata: bool) -> Dict[str, Any]:
        """Format as CSV"""
        if not isinstance(data, pd.DataFrame):
            if isinstance(data, list):
                data = pd.DataFrame(data)
            else:
                data = pd.DataFrame([{'value': data}])
        
        csv_content = data.to_csv(index=False)
        
        result = {
            'format': 'csv',
            'content': csv_content,
            'record_count': len(data)
        }
        
        if include_metadata:
            result['metadata'] = {
                'format': 'csv',
                'columns': list(data.columns),
                'row_count': len(data),
                'delimiter': ','
            }
        
        return result
    
    def _format_json(self, data: Any, include_metadata: bool) -> Dict[str, Any]:
        """Format as JSON"""
        if isinstance(data, pd.DataFrame):
            records = data.to_dict('records')
        elif isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = [data]
        else:
            records = [{'value': data}]
        
        json_content = json.dumps(records, indent=2, default=str)
        
        result = {
            'format': 'json',
            'content': json_content,
            'record_count': len(records)
        }
        
        if include_metadata:
            result['metadata'] = {
                'format': 'json',
                'encoding': 'utf-8',
                'record_count': len(records)
            }
        
        return result

