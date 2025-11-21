"""
Redaction pipeline - orchestrates PII detection and redaction
"""
from typing import Any, Dict, List, Optional
import pandas as pd
from .pii_detector import PIIDetector
from .redactor import DataRedactor


class RedactionPipeline:
    """Orchestrates PII/PHI detection and redaction"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.detector = PIIDetector(self.config.get('detection', {}))
        self.redactor = DataRedactor(self.config.get('redaction', {}))
    
    def process(self, data: Any, entity_types: Optional[List[str]] = None,
                columns: Optional[List[str]] = None, 
                detect_only: bool = False) -> Dict[str, Any]:
        """
        Process data through detection and redaction
        
        Args:
            data: Data to process
            entity_types: Specific entity types to process
            columns: Specific columns to process (for DataFrames)
            detect_only: If True, only detect without redacting
        
        Returns:
            Dict with processed data and statistics
        """
        results = {
            'original_data': data,
            'detection': None,
            'redaction': None,
            'stats': {}
        }
        
        # Step 1: Detect PII/PHI
        detection_result = self.detector.detect(data, entity_types)
        results['detection'] = detection_result
        
        # Step 2: Redact if not detect-only
        if not detect_only and detection_result.get('count', 0) > 0:
            redaction_result = self.redactor.redact(data, entity_types, columns)
            results['redaction'] = redaction_result
            results['processed_data'] = redaction_result['data']
        else:
            results['processed_data'] = data
        
        # Aggregate statistics
        results['stats'] = {
            'entities_detected': detection_result.get('count', 0),
            'entities_redacted': results['redaction']['stats']['entities_redacted'] 
                                if results['redaction'] else 0,
            'entity_summary': detection_result.get('summary', {})
        }
        
        return results

