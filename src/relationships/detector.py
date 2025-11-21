"""
Relationship detector for discovering connections between files
"""
from typing import Dict, Any, List, Optional
from loguru import logger

from .strategies import (
    FilenameStrategy,
    ContentStrategy,
    MetadataStrategy,
    SemanticStrategy
)


class RelationshipDetector:
    """Detect relationships between files"""
    
    RELATIONSHIP_TYPES = {
        'INFORMS': 'File A provides data/information used in File B',
        'SUMMARIZES': 'File A summarizes or presents data from File B',
        'DOCUMENTS': 'File A documents or explains File B',
        'REFERENCES': 'File A references data from File B',
        'RELATED_TO': 'Files share common context or topic'
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.min_confidence = self.config.get('min_confidence', 0.7)
        
        # Initialize strategies
        self.strategies = []
        
        if self.config.get('use_filename_strategy', True):
            self.strategies.append(FilenameStrategy())
        
        if self.config.get('use_content_strategy', True):
            self.strategies.append(ContentStrategy())
        
        if self.config.get('use_metadata_strategy', True):
            self.strategies.append(MetadataStrategy())
        
        if self.config.get('use_semantic_strategy', False):  # Optional, requires sentence-transformers
            try:
                self.strategies.append(SemanticStrategy())
            except Exception:
                logger.warning("Semantic strategy not available (sentence-transformers not installed)")
    
    def detect_relationships(
        self,
        file_metadata_list: List[Dict[str, Any]],
        strategies: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Detect relationships between all files
        
        Args:
            file_metadata_list: List of file metadata dictionaries
            strategies: Optional list of strategy names to use
        
        Returns:
            List of detected relationships
        """
        relationships = []
        total_pairs = len(file_metadata_list) * (len(file_metadata_list) - 1) // 2
        
        logger.info(f"Detecting relationships between {len(file_metadata_list)} files ({total_pairs} pairs)")
        
        # Compare all pairs
        for i, file1 in enumerate(file_metadata_list):
            for j, file2 in enumerate(file_metadata_list[i+1:], start=i+1):
                relationship = self._detect_relationship(file1, file2)
                if relationship:
                    relationships.append(relationship)
        
        # Filter by confidence threshold
        filtered = [r for r in relationships if r['confidence'] >= self.min_confidence]
        
        logger.info(f"Found {len(filtered)} relationships (confidence >= {self.min_confidence})")
        
        return filtered
    
    def _detect_relationship(
        self,
        file1_metadata: Dict[str, Any],
        file2_metadata: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Detect relationship between two files using all strategies"""
        all_evidence = []
        best_relationship = None
        best_confidence = 0.0
        
        # Try each strategy
        for strategy in self.strategies:
            try:
                result = strategy.detect(file1_metadata, file2_metadata)
                if result:
                    all_evidence.append({
                        'strategy': strategy.__class__.__name__,
                        'evidence': result.get('evidence', {})
                    })
                    
                    # Take the best confidence score
                    if result['confidence'] > best_confidence:
                        best_confidence = result['confidence']
                        best_relationship = result['relationship_type']
            except Exception as e:
                logger.debug(f"Strategy {strategy.__class__.__name__} failed: {e}")
                continue
        
        # If we found a relationship, combine evidence
        if best_relationship and best_confidence >= self.min_confidence:
            return {
                'source_file_id': file1_metadata.get('file_id'),
                'source_file_name': file1_metadata.get('file_name'),
                'target_file_id': file2_metadata.get('file_id'),
                'target_file_name': file2_metadata.get('file_name'),
                'relationship_type': best_relationship,
                'relationship_description': self.RELATIONSHIP_TYPES.get(best_relationship, ''),
                'confidence': best_confidence,
                'evidence': all_evidence,
                'evidence_count': len(all_evidence)
            }
        
        return None
    
    def get_relationship_summary(self, relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics about relationships"""
        if not relationships:
            return {
                'total_relationships': 0,
                'by_type': {},
                'average_confidence': 0.0
            }
        
        by_type = {}
        total_confidence = 0.0
        
        for rel in relationships:
            rel_type = rel['relationship_type']
            by_type[rel_type] = by_type.get(rel_type, 0) + 1
            total_confidence += rel['confidence']
        
        return {
            'total_relationships': len(relationships),
            'by_type': by_type,
            'average_confidence': round(total_confidence / len(relationships), 3),
            'min_confidence': round(min(r['confidence'] for r in relationships), 3),
            'max_confidence': round(max(r['confidence'] for r in relationships), 3)
        }

