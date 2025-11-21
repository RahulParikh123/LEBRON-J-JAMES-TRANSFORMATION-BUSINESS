"""
JSON file handler
"""
from typing import Dict, Any, List, Union
import json
import pandas as pd
from pathlib import Path
from .base_handler import BaseHandler


class JSONHandler(BaseHandler):
    """Handler for JSON files"""
    
    def can_handle(self, file_path: str) -> bool:
        """Check if file is a JSON file"""
        ext = Path(file_path).suffix.lower()
        return ext == '.json'
    
    def get_supported_extensions(self) -> List[str]:
        return ['.json']
    
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        """Extract data from JSON file"""
        metadata = self.extract_metadata(source)
        
        try:
            with open(source, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                # Array of objects
                records = data
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Single object or nested structure
                if self._is_record_like(data):
                    records = [data]
                    df = pd.DataFrame([data])
                else:
                    # Nested structure - flatten if possible
                    records = self._flatten_dict(data)
                    df = pd.DataFrame(records) if records else pd.DataFrame()
            else:
                records = [{'value': data}]
                df = pd.DataFrame([{'value': data}])
            
            if not df.empty:
                df = self.normalize_dataframe(df)
                records = df.to_dict('records')
            
            # Generate text representation
            text_content = self._json_to_text(data)
            
            metadata.update({
                'row_count': len(records),
                'structure_type': self._detect_structure_type(data)
            })
            
            return {
                'data': records,
                'metadata': metadata,
                'text_content': [text_content],
                'structure': {
                    'format': 'json',
                    'structure_type': self._detect_structure_type(data),
                    'columns': list(df.columns) if not df.empty else []
                }
            }
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in file {source}: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error reading JSON file {source}: {str(e)}")
    
    def _is_record_like(self, obj: Dict) -> bool:
        """Check if dict looks like a record (flat or mostly flat)"""
        if not isinstance(obj, dict):
            return False
        
        # Check if values are mostly primitive types
        primitive_count = sum(1 for v in obj.values() 
                             if isinstance(v, (str, int, float, bool, type(None))))
        return primitive_count / len(obj) > 0.7 if obj else False
    
    def _flatten_dict(self, data: Dict, parent_key: str = '', sep: str = '_') -> List[Dict]:
        """Flatten nested dictionary structure"""
        items = []
        
        def _flatten(obj, parent=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    new_key = f"{parent}{sep}{k}" if parent else k
                    if isinstance(v, dict):
                        _flatten(v, new_key)
                    elif isinstance(v, list):
                        for i, item in enumerate(v):
                            if isinstance(item, dict):
                                _flatten(item, f"{new_key}{sep}{i}")
                            else:
                                items.append({new_key: item})
                    else:
                        items.append({new_key: v})
            else:
                items.append({parent: obj})
        
        _flatten(data, parent_key)
        return items if items else [data]
    
    def _detect_structure_type(self, data: Any) -> str:
        """Detect the type of JSON structure"""
        if isinstance(data, list):
            return 'array'
        elif isinstance(data, dict):
            if self._is_record_like(data):
                return 'object'
            else:
                return 'nested_object'
        else:
            return 'primitive'
    
    def _json_to_text(self, data: Any, indent: int = 0) -> str:
        """Convert JSON to text representation"""
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{'  ' * indent}{key}:")
                    lines.append(self._json_to_text(value, indent + 1))
                else:
                    lines.append(f"{'  ' * indent}{key}: {value}")
            return "\n".join(lines)
        elif isinstance(data, list):
            lines = []
            for i, item in enumerate(data[:10]):  # Limit to first 10 items
                lines.append(f"Item {i}:")
                lines.append(self._json_to_text(item, indent + 1))
            return "\n".join(lines)
        else:
            return f"{'  ' * indent}{data}"

