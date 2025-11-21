"""
Data redaction module - remove or mask PII/PHI
"""
from typing import Any, Dict, List, Optional
import pandas as pd
import numpy as np
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from .pii_detector import PIIDetector


class DataRedactor:
    """Redact PII/PHI from data"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.detector = PIIDetector(config)
        
        # Redaction strategy: 'remove', 'mask', 'hash', 'replace'
        self.strategy = self.config.get('strategy', 'mask')
        
        # Initialize Presidio anonymizer
        try:
            self.anonymizer = AnonymizerEngine()
        except Exception as e:
            print(f"Warning: Presidio anonymizer not fully initialized: {e}")
            self.anonymizer = None
    
    def redact(self, data: Any, entity_types: Optional[List[str]] = None,
               columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Redact PII/PHI from data
        
        Args:
            data: DataFrame, list, or string
            entity_types: Specific entity types to redact
            columns: Specific columns to redact (if None, redacts all)
        
        Returns:
            Dict with redacted data and statistics
        """
        if isinstance(data, pd.DataFrame):
            return self._redact_dataframe(data, entity_types, columns)
        elif isinstance(data, list):
            return self._redact_list(data, entity_types)
        elif isinstance(data, str):
            return self._redact_text(data, entity_types)
        else:
            return {'data': data, 'stats': {'entities_redacted': 0}}
    
    def _redact_dataframe(self, df: pd.DataFrame, entity_types: Optional[List[str]] = None,
                         columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """Redact PII from DataFrame"""
        df_redacted = df.copy()
        stats = {
            'entities_redacted': 0,
            'columns_processed': 0,
            'rows_modified': 0
        }
        
        # Determine columns to process
        cols_to_process = columns if columns else df.columns.tolist()
        
        for col in cols_to_process:
            if col not in df.columns:
                continue
            
            col_stats = self._redact_column(df_redacted[col], entity_types)
            df_redacted[col] = col_stats['data']
            
            stats['entities_redacted'] += col_stats['entities_redacted']
            stats['columns_processed'] += 1
            if col_stats['entities_redacted'] > 0:
                stats['rows_modified'] += col_stats['rows_modified']
        
        return {
            'data': df_redacted,
            'stats': stats
        }
    
    def _redact_column(self, series: pd.Series, entity_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Redact PII from a pandas Series"""
        redacted_series = series.copy()
        entities_redacted = 0
        rows_modified = 0
        
        for idx, value in series.items():
            if pd.notna(value):
                text = str(value)
                result = self._redact_text(text, entity_types)
                
                if result['entities_redacted'] > 0:
                    redacted_series.at[idx] = result['data']
                    entities_redacted += result['entities_redacted']
                    rows_modified += 1
        
        return {
            'data': redacted_series,
            'entities_redacted': entities_redacted,
            'rows_modified': rows_modified
        }
    
    def _redact_list(self, data: List, entity_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Redact PII from list of records"""
        redacted_data = []
        entities_redacted = 0
        
        for item in data:
            if isinstance(item, dict):
                redacted_item = {}
                for key, value in item.items():
                    if isinstance(value, (str, int, float)):
                        result = self._redact_text(str(value), entity_types)
                        redacted_item[key] = result['data']
                        entities_redacted += result['entities_redacted']
                    else:
                        redacted_item[key] = value
                redacted_data.append(redacted_item)
            elif isinstance(item, str):
                result = self._redact_text(item, entity_types)
                redacted_data.append(result['data'])
                entities_redacted += result['entities_redacted']
            else:
                redacted_data.append(item)
        
        return {
            'data': redacted_data,
            'stats': {'entities_redacted': entities_redacted}
        }
    
    def _redact_text(self, text: str, entity_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Redact PII from text"""
        # First detect entities
        detection_result = self.detector._detect_text(text, entity_types)
        entities = detection_result.get('entities', [])
        
        if not entities:
            return {'data': text, 'entities_redacted': 0}
        
        # Use Presidio anonymizer if available
        if self.anonymizer and self.strategy == 'mask':
            try:
                # Convert to Presidio format
                analyzer_results = []
                for entity in entities:
                    from presidio_analyzer import RecognizerResult
                    analyzer_results.append(
                        RecognizerResult(
                            entity_type=entity['type'],
                            start=entity['start'],
                            end=entity['end'],
                            score=entity['score']
                        )
                    )
                
                anonymized = self.anonymizer.anonymize(
                    text=text,
                    analyzer_results=analyzer_results
                )
                return {
                    'data': anonymized.text,
                    'entities_redacted': len(entities)
                }
            except Exception:
                # Fallback to custom redaction
                pass
        
        # Custom redaction based on strategy
        redacted_text = text
        offset = 0
        
        # Sort entities by position (reverse for safe replacement)
        sorted_entities = sorted(entities, key=lambda x: x['start'], reverse=True)
        
        for entity in sorted_entities:
            start = entity['start']
            end = entity['end']
            replacement = self._get_replacement(entity['type'], entity['text'])
            
            redacted_text = redacted_text[:start] + replacement + redacted_text[end:]
        
        return {
            'data': redacted_text,
            'entities_redacted': len(entities)
        }
    
    def _get_replacement(self, entity_type: str, original_text: str) -> str:
        """Get replacement text based on strategy and entity type"""
        if self.strategy == 'remove':
            return ''
        elif self.strategy == 'hash':
            import hashlib
            return hashlib.sha256(original_text.encode()).hexdigest()[:8]
        elif self.strategy == 'replace':
            replacements = {
                'EMAIL': '[EMAIL]',
                'PHONE': '[PHONE]',
                'SSN': '[SSN]',
                'CREDIT_CARD': '[CARD]',
                'PERSON': '[PERSON]',
                'IP_ADDRESS': '[IP]',
            }
            return replacements.get(entity_type, '[REDACTED]')
        else:  # mask (default)
            # Mask with asterisks, preserving length
            return '*' * len(original_text)

