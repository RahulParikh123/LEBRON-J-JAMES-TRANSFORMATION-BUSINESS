"""
Data validation module
"""
from typing import Any, Dict, List, Optional, Callable
import pandas as pd
import numpy as np
from datetime import datetime
import re


class DataValidator:
    """Validate data quality and structure"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.validation_rules = self.config.get('rules', {})
        self.validation_results = []
    
    def validate(self, data: Any, schema: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Validate data against schema and rules
        
        Returns validation results with issues found
        """
        if isinstance(data, pd.DataFrame):
            return self._validate_dataframe(data, schema)
        elif isinstance(data, list):
            return self._validate_list(data, schema)
        else:
            return {'valid': True, 'issues': []}
    
    def _validate_dataframe(self, df: pd.DataFrame, schema: Optional[Dict] = None) -> Dict[str, Any]:
        """Validate DataFrame"""
        issues = []
        
        # 1. Check for empty DataFrame
        if df.empty:
            issues.append({
                'type': 'empty_dataframe',
                'severity': 'error',
                'message': 'DataFrame is empty'
            })
            return {'valid': False, 'issues': issues}
        
        # 2. Check for required columns if schema provided
        if schema and 'required_columns' in schema:
            missing_cols = set(schema['required_columns']) - set(df.columns)
            if missing_cols:
                issues.append({
                    'type': 'missing_columns',
                    'severity': 'error',
                    'message': f'Missing required columns: {missing_cols}',
                    'columns': list(missing_cols)
                })
        
        # 3. Validate data types if schema provided
        if schema and 'column_types' in schema:
            type_issues = self._validate_types(df, schema['column_types'])
            issues.extend(type_issues)
        
        # 4. Check for null values
        null_issues = self._validate_null_values(df, schema)
        issues.extend(null_issues)
        
        # 5. Validate data ranges/constraints
        constraint_issues = self._validate_constraints(df, schema)
        issues.extend(constraint_issues)
        
        # 6. Validate data formats (email, phone, etc.)
        format_issues = self._validate_formats(df, schema)
        issues.extend(format_issues)
        
        # Determine overall validity
        has_errors = any(issue['severity'] == 'error' for issue in issues)
        valid = not has_errors
        
        return {
            'valid': valid,
            'issues': issues,
            'summary': {
                'total_issues': len(issues),
                'errors': sum(1 for i in issues if i['severity'] == 'error'),
                'warnings': sum(1 for i in issues if i['severity'] == 'warning'),
                'info': sum(1 for i in issues if i['severity'] == 'info')
            }
        }
    
    def _validate_list(self, data: List, schema: Optional[Dict] = None) -> Dict[str, Any]:
        """Validate list of records"""
        if not data:
            return {'valid': False, 'issues': [{'type': 'empty_list', 'severity': 'error'}]}
        
        # Convert to DataFrame for validation
        try:
            df = pd.DataFrame(data)
            return self._validate_dataframe(df, schema)
        except Exception as e:
            return {
                'valid': False,
                'issues': [{
                    'type': 'conversion_error',
                    'severity': 'error',
                    'message': f'Cannot convert to DataFrame: {str(e)}'
                }]
            }
    
    def _validate_types(self, df: pd.DataFrame, column_types: Dict[str, str]) -> List[Dict]:
        """Validate column data types"""
        issues = []
        
        for col, expected_type in column_types.items():
            if col not in df.columns:
                continue
            
            actual_type = str(df[col].dtype)
            expected_dtype = self._map_type_string(expected_type)
            
            if not self._type_compatible(actual_type, expected_dtype):
                issues.append({
                    'type': 'type_mismatch',
                    'severity': 'error',
                    'column': col,
                    'expected': expected_type,
                    'actual': actual_type,
                    'message': f'Column {col} has type {actual_type}, expected {expected_type}'
                })
        
        return issues
    
    def _validate_null_values(self, df: pd.DataFrame, schema: Optional[Dict] = None) -> List[Dict]:
        """Validate null values"""
        issues = []
        
        null_counts = df.isnull().sum()
        
        for col in df.columns:
            null_count = null_counts[col]
            null_percentage = (null_count / len(df)) * 100
            
            # Check schema constraints
            if schema and 'columns' in schema and col in schema['columns']:
                col_schema = schema['columns'][col]
                max_null_pct = col_schema.get('max_null_percentage', 100)
                required = col_schema.get('required', False)
                
                if required and null_count > 0:
                    issues.append({
                        'type': 'required_null',
                        'severity': 'error',
                        'column': col,
                        'null_count': int(null_count),
                        'message': f'Required column {col} has {null_count} null values'
                    })
                elif null_percentage > max_null_pct:
                    issues.append({
                        'type': 'excessive_nulls',
                        'severity': 'warning',
                        'column': col,
                        'null_count': int(null_count),
                        'null_percentage': round(null_percentage, 2),
                        'message': f'Column {col} has {null_percentage:.2f}% null values'
                    })
            elif null_percentage > 50:
                # Default: warn if more than 50% nulls
                issues.append({
                    'type': 'excessive_nulls',
                    'severity': 'warning',
                    'column': col,
                    'null_count': int(null_count),
                    'null_percentage': round(null_percentage, 2)
                })
        
        return issues
    
    def _validate_constraints(self, df: pd.DataFrame, schema: Optional[Dict] = None) -> List[Dict]:
        """Validate data constraints (ranges, min/max, etc.)"""
        issues = []
        
        if not schema or 'columns' not in schema:
            return issues
        
        for col, col_schema in schema['columns'].items():
            if col not in df.columns:
                continue
            
            # Check min/max values
            if 'min_value' in col_schema:
                min_val = col_schema['min_value']
                below_min = df[df[col] < min_val]
                if len(below_min) > 0:
                    issues.append({
                        'type': 'below_minimum',
                        'severity': 'error',
                        'column': col,
                        'min_value': min_val,
                        'count': len(below_min)
                    })
            
            if 'max_value' in col_schema:
                max_val = col_schema['max_value']
                above_max = df[df[col] > max_val]
                if len(above_max) > 0:
                    issues.append({
                        'type': 'above_maximum',
                        'severity': 'error',
                        'column': col,
                        'max_value': max_val,
                        'count': len(above_max)
                    })
            
            # Check unique constraint
            if col_schema.get('unique', False):
                duplicates = df[col].duplicated()
                if duplicates.any():
                    issues.append({
                        'type': 'duplicate_values',
                        'severity': 'error',
                        'column': col,
                        'count': int(duplicates.sum()),
                        'message': f'Column {col} should be unique but has duplicates'
                    })
        
        return issues
    
    def _validate_formats(self, df: pd.DataFrame, schema: Optional[Dict] = None) -> List[Dict]:
        """Validate data formats (email, phone, date, etc.)"""
        issues = []
        
        if not schema or 'columns' not in schema:
            return issues
        
        format_patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^[\d\s\-\+\(\)]+$',
            'url': r'^https?://.+',
            'date': r'^\d{4}-\d{2}-\d{2}',
        }
        
        for col, col_schema in schema['columns'].items():
            if col not in df.columns:
                continue
            
            format_type = col_schema.get('format')
            if not format_type:
                continue
            
            pattern = format_patterns.get(format_type)
            if not pattern:
                continue
            
            invalid = df[df[col].notna() & ~df[col].astype(str).str.match(pattern, na=False)]
            if len(invalid) > 0:
                issues.append({
                    'type': 'format_mismatch',
                    'severity': 'warning',
                    'column': col,
                    'format': format_type,
                    'count': len(invalid),
                    'message': f'Column {col} has {len(invalid)} values not matching {format_type} format'
                })
        
        return issues
    
    def _map_type_string(self, type_str: str) -> str:
        """Map type string to pandas dtype"""
        mapping = {
            'string': 'object',
            'int': 'int64',
            'float': 'float64',
            'bool': 'bool',
            'datetime': 'datetime64[ns]',
            'date': 'datetime64[ns]',
        }
        return mapping.get(type_str.lower(), type_str)
    
    def _type_compatible(self, actual: str, expected: str) -> bool:
        """Check if actual type is compatible with expected"""
        if actual == expected:
            return True
        
        # Allow some flexibility
        if 'int' in actual and 'int' in expected:
            return True
        if 'float' in actual and 'float' in expected:
            return True
        if actual == 'object' and expected == 'object':
            return True
        
        return False

