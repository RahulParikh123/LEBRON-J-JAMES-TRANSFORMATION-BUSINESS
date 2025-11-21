"""
PII/PHI detection module using Presidio
"""
from typing import Any, Dict, List, Optional, Set
import pandas as pd
import re

# Presidio will be imported lazily to avoid compatibility issues
PRESIDIO_AVAILABLE = None
AnalyzerEngine = None


class PIIDetector:
    """Detect PII/PHI in data"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Initialize Presidio analyzer (lazy import to avoid compatibility issues)
        self.analyzer = None
        self._try_init_presidio()
        
        # Custom patterns for additional detection
        self.custom_patterns = self._load_custom_patterns()
    
    def _try_init_presidio(self):
        """Try to initialize Presidio analyzer (lazy import)"""
        global PRESIDIO_AVAILABLE, AnalyzerEngine
        
        if PRESIDIO_AVAILABLE is None:
            # First time - try to import
            try:
                from presidio_analyzer import AnalyzerEngine as _AnalyzerEngine
                AnalyzerEngine = _AnalyzerEngine
                PRESIDIO_AVAILABLE = True
            except (ImportError, Exception) as e:
                PRESIDIO_AVAILABLE = False
                AnalyzerEngine = None
                print(f"Warning: Presidio not available ({type(e).__name__}). PII detection will use pattern matching only.")
        
        # Now try to create analyzer instance
        if PRESIDIO_AVAILABLE and AnalyzerEngine:
            try:
                self.analyzer = AnalyzerEngine()
            except Exception as e:
                print(f"Warning: Presidio analyzer initialization failed: {e}")
                print("Note: PII detection will use pattern matching only")
                self.analyzer = None
    
    def detect(self, data: Any, entity_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Detect PII/PHI in data
        
        Args:
            data: DataFrame, list, or string
            entity_types: Specific entity types to detect (if None, detects all)
        
        Returns:
            Dict with detected entities and locations
        """
        if isinstance(data, pd.DataFrame):
            return self._detect_dataframe(data, entity_types)
        elif isinstance(data, list):
            return self._detect_list(data, entity_types)
        elif isinstance(data, str):
            return self._detect_text(data, entity_types)
        else:
            return {'entities': [], 'count': 0}
    
    def _detect_dataframe(self, df: pd.DataFrame, entity_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Detect PII in DataFrame"""
        all_entities = []
        column_entities = {}
        
        for col in df.columns:
            col_entities = []
            
            for idx, value in df[col].items():
                if pd.notna(value):
                    text = str(value)
                    entities = self._detect_text(text, entity_types)
                    
                    for entity in entities.get('entities', []):
                        entity['row'] = idx
                        entity['column'] = col
                        col_entities.append(entity)
                        all_entities.append(entity)
            
            if col_entities:
                column_entities[col] = col_entities
        
        return {
            'entities': all_entities,
            'count': len(all_entities),
            'by_column': column_entities,
            'summary': self._summarize_entities(all_entities)
        }
    
    def _detect_list(self, data: List, entity_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Detect PII in list of records"""
        all_entities = []
        
        for idx, item in enumerate(data):
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, (str, int, float)):
                        text = str(value)
                        entities = self._detect_text(text, entity_types)
                        for entity in entities.get('entities', []):
                            entity['record_index'] = idx
                            entity['field'] = key
                            all_entities.append(entity)
            elif isinstance(item, str):
                entities = self._detect_text(item, entity_types)
                for entity in entities.get('entities', []):
                    entity['record_index'] = idx
                    all_entities.append(entity)
        
        return {
            'entities': all_entities,
            'count': len(all_entities),
            'summary': self._summarize_entities(all_entities)
        }
    
    def _detect_text(self, text: str, entity_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Detect PII in text using Presidio and custom patterns"""
        entities = []
        
        # Use Presidio if available
        if self.analyzer:
            try:
                presidio_results = self.analyzer.analyze(
                    text=text,
                    entities=entity_types,
                    language='en'
                )
                
                for result in presidio_results:
                    entities.append({
                        'type': result.entity_type,
                        'start': result.start,
                        'end': result.end,
                        'score': result.score,
                        'text': text[result.start:result.end],
                        'detector': 'presidio'
                    })
            except Exception as e:
                # Fallback to pattern matching
                pass
        
        # Use custom patterns
        custom_entities = self._detect_custom_patterns(text)
        entities.extend(custom_entities)
        
        # Remove duplicates (same position)
        unique_entities = self._deduplicate_entities(entities)
        
        return {
            'entities': unique_entities,
            'count': len(unique_entities)
        }
    
    def _detect_custom_patterns(self, text: str) -> List[Dict]:
        """Detect PII using custom regex patterns"""
        entities = []
        
        for pattern_name, pattern_info in self.custom_patterns.items():
            pattern = pattern_info['pattern']
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                entities.append({
                    'type': pattern_name,
                    'start': match.start(),
                    'end': match.end(),
                    'score': pattern_info.get('confidence', 0.8),
                    'text': match.group(),
                    'detector': 'custom_pattern'
                })
        
        return entities
    
    def _load_custom_patterns(self) -> Dict[str, Dict]:
        """Load custom PII detection patterns"""
        return {
            'SSN': {
                'pattern': r'\b\d{3}-\d{2}-\d{4}\b',
                'confidence': 0.9
            },
            'CREDIT_CARD': {
                'pattern': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
                'confidence': 0.85
            },
            'IP_ADDRESS': {
                'pattern': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
                'confidence': 0.7
            },
            'PHONE': {
                'pattern': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                'confidence': 0.75
            },
            'EMAIL': {
                'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                'confidence': 0.8
            },
        }
    
    def _deduplicate_entities(self, entities: List[Dict]) -> List[Dict]:
        """Remove duplicate entities at the same position"""
        seen = set()
        unique = []
        
        for entity in entities:
            key = (entity['start'], entity['end'], entity['type'])
            if key not in seen:
                seen.add(key)
                unique.append(entity)
        
        return unique
    
    def _summarize_entities(self, entities: List[Dict]) -> Dict[str, int]:
        """Summarize detected entities by type"""
        summary = {}
        for entity in entities:
            entity_type = entity['type']
            summary[entity_type] = summary.get(entity_type, 0) + 1
        return summary

