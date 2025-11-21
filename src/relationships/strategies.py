"""
Relationship detection strategies
"""
from typing import Dict, Any, List, Optional, Set
from pathlib import Path
import re
from difflib import SequenceMatcher


class BaseStrategy:
    """Base class for relationship detection strategies"""
    
    def detect(self, file1_metadata: Dict[str, Any], file2_metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect relationship between two files"""
        raise NotImplementedError
    
    def get_confidence(self, evidence: Dict[str, Any]) -> float:
        """Calculate confidence score from evidence"""
        raise NotImplementedError


class FilenameStrategy(BaseStrategy):
    """Detect relationships based on filename patterns"""
    
    def detect(self, file1_metadata: Dict[str, Any], file2_metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect relationship based on filename similarity"""
        name1 = Path(file1_metadata['file_name']).stem.lower()
        name2 = Path(file2_metadata['file_name']).stem.lower()
        
        # Extract base name (remove version numbers, dates, etc.)
        base1 = self._extract_base_name(name1)
        base2 = self._extract_base_name(name2)
        
        # Check for similarity
        similarity = SequenceMatcher(None, base1, base2).ratio()
        
        if similarity > 0.6:  # 60% similarity threshold
            # Determine relationship type
            rel_type = self._determine_relationship_type(name1, name2)
            
            return {
                'relationship_type': rel_type,
                'confidence': min(similarity, 0.9),  # Cap at 0.9
                'evidence': {
                    'filename_similarity': similarity,
                    'base_name_match': base1 == base2,
                    'file1_name': file1_metadata['file_name'],
                    'file2_name': file2_metadata['file_name']
                }
            }
        
        return None
    
    def _extract_base_name(self, filename: str) -> str:
        """Extract base name from filename (remove dates, versions, etc.)"""
        # Remove common suffixes
        patterns = [
            r'_\d{4}-\d{2}-\d{2}',  # Dates
            r'_v\d+',  # Versions
            r'_final', r'_draft', r'_rev\d+',
            r'\(.*?\)',  # Parentheses content
        ]
        
        base = filename
        for pattern in patterns:
            base = re.sub(pattern, '', base, flags=re.IGNORECASE)
        
        return base.strip('_-.')
    
    def _determine_relationship_type(self, name1: str, name2: str) -> str:
        """Determine relationship type from filenames"""
        name1_lower = name1.lower()
        name2_lower = name2.lower()
        
        # Check for presentation/deck keywords
        if any(word in name1_lower for word in ['presentation', 'deck', 'ppt', 'slides']):
            if any(word in name2_lower for word in ['data', 'model', 'analysis', 'report']):
                return 'SUMMARIZES'
        
        # Check for model/analysis keywords
        if any(word in name1_lower for word in ['model', 'analysis', 'data']):
            if any(word in name2_lower for word in ['presentation', 'deck', 'report']):
                return 'INFORMS'
        
        # Default to RELATED_TO
        return 'RELATED_TO'


class ContentStrategy(BaseStrategy):
    """Detect relationships based on shared content"""
    
    def __init__(self, min_shared_entities: int = 2, min_shared_terms: int = 3):
        self.min_shared_entities = min_shared_entities
        self.min_shared_terms = min_shared_terms
    
    def detect(self, file1_metadata: Dict[str, Any], file2_metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect relationship based on shared content"""
        entities1 = set(file1_metadata.get('entities', []) or [])
        entities2 = set(file2_metadata.get('entities', []) or [])
        terms1 = set(file1_metadata.get('key_terms', []) or [])
        terms2 = set(file2_metadata.get('key_terms', []) or [])
        
        shared_entities = entities1.intersection(entities2)
        shared_terms = terms1.intersection(terms2)
        
        evidence = {
            'shared_entities': list(shared_entities),
            'shared_terms': list(shared_terms),
            'shared_entity_count': len(shared_entities),
            'shared_term_count': len(shared_terms)
        }
        
        # Check if we have enough shared content
        has_entities = len(shared_entities) >= self.min_shared_entities
        has_terms = len(shared_terms) >= self.min_shared_terms
        
        if has_entities or has_terms:
            # Calculate confidence
            entity_score = min(len(shared_entities) / 10.0, 1.0)  # Normalize
            term_score = min(len(shared_terms) / 15.0, 1.0)  # Normalize
            
            confidence = (entity_score * 0.6 + term_score * 0.4)
            confidence = max(0.7, min(confidence, 0.95))  # Clamp between 0.7 and 0.95
            
            # Determine relationship type
            rel_type = self._determine_relationship_type(
                file1_metadata, file2_metadata, shared_entities, shared_terms
            )
            
            return {
                'relationship_type': rel_type,
                'confidence': confidence,
                'evidence': evidence
            }
        
        return None
    
    def _determine_relationship_type(
        self,
        file1_metadata: Dict[str, Any],
        file2_metadata: Dict[str, Any],
        shared_entities: Set[str],
        shared_terms: Set[str]
    ) -> str:
        """Determine relationship type from content"""
        type1 = file1_metadata.get('file_type', '')
        type2 = file2_metadata.get('file_type', '')
        
        # Excel -> PowerPoint: INFORMS
        if type1 == 'excel' and type2 == 'powerpoint':
            return 'INFORMS'
        
        # Word -> Excel: INFORMS
        if type1 == 'word' and type2 == 'excel':
            return 'INFORMS'
        
        # PowerPoint -> Word: DOCUMENTS
        if type1 == 'powerpoint' and type2 == 'word':
            return 'DOCUMENTS'
        
        # Excel -> Word: DOCUMENTS
        if type1 == 'excel' and type2 == 'word':
            return 'DOCUMENTS'
        
        # PowerPoint -> Excel: SUMMARIZES (PPT summarizes Excel data)
        if type1 == 'powerpoint' and type2 == 'excel':
            return 'SUMMARIZES'
        
        # Default based on shared content strength
        if len(shared_entities) >= 5:
            return 'INFORMS'
        
        return 'RELATED_TO'


class MetadataStrategy(BaseStrategy):
    """Detect relationships based on metadata"""
    
    def detect(self, file1_metadata: Dict[str, Any], file2_metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect relationship based on metadata"""
        evidence = {}
        score = 0.0
        
        # Same author
        author1 = file1_metadata.get('author')
        author2 = file2_metadata.get('author')
        if author1 and author2 and author1.lower() == author2.lower():
            evidence['same_author'] = author1
            score += 0.2
        
        # Same title/subject
        title1 = file1_metadata.get('title', '').lower()
        title2 = file2_metadata.get('title', '').lower()
        if title1 and title2:
            similarity = SequenceMatcher(None, title1, title2).ratio()
            if similarity > 0.7:
                evidence['title_similarity'] = similarity
                score += 0.3
        
        # Temporal proximity (created within 7 days)
        created1 = file1_metadata.get('created_at')
        created2 = file2_metadata.get('created_at')
        if created1 and created2:
            try:
                from datetime import datetime
                dt1 = datetime.fromisoformat(created1.replace('Z', '+00:00'))
                dt2 = datetime.fromisoformat(created2.replace('Z', '+00:00'))
                days_diff = abs((dt1 - dt2).days)
                if days_diff <= 7:
                    evidence['temporal_proximity_days'] = days_diff
                    score += 0.2
            except Exception:
                pass
        
        # Same directory
        path1 = Path(file1_metadata.get('file_path', ''))
        path2 = Path(file2_metadata.get('file_path', ''))
        if path1.parent == path2.parent:
            evidence['same_directory'] = True
            score += 0.1
        
        if score >= 0.4:  # Threshold for metadata-based relationship
            return {
                'relationship_type': 'RELATED_TO',
                'confidence': min(score, 0.85),
                'evidence': evidence
            }
        
        return None


class SemanticStrategy(BaseStrategy):
    """Detect relationships based on semantic similarity (using embeddings)"""
    
    def __init__(self):
        self.embeddings_model = None
        self._try_load_model()
    
    def _try_load_model(self):
        """Try to load sentence-transformers model"""
        try:
            from sentence_transformers import SentenceTransformer
            self.embeddings_model = SentenceTransformer('all-MiniLM-L6-v2')
        except ImportError:
            # Model not available, will use fallback
            pass
    
    def detect(self, file1_metadata: Dict[str, Any], file2_metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect relationship based on semantic similarity"""
        if not self.embeddings_model:
            return None  # Can't use semantic similarity without model
        
        # Create text representation from metadata
        text1 = self._create_text_representation(file1_metadata)
        text2 = self._create_text_representation(file2_metadata)
        
        if not text1 or not text2:
            return None
        
        try:
            # Compute embeddings
            embeddings1 = self.embeddings_model.encode(text1)
            embeddings2 = self.embeddings_model.encode(text2)
            
            # Compute cosine similarity
            import numpy as np
            similarity = np.dot(embeddings1, embeddings2) / (
                np.linalg.norm(embeddings1) * np.linalg.norm(embeddings2)
            )
            
            if similarity >= 0.7:  # Threshold
                return {
                    'relationship_type': 'RELATED_TO',
                    'confidence': float(similarity),
                    'evidence': {
                        'semantic_similarity': float(similarity)
                    }
                }
        except Exception:
            pass
        
        return None
    
    def _create_text_representation(self, metadata: Dict[str, Any]) -> str:
        """Create text representation from metadata"""
        parts = []
        
        if metadata.get('title'):
            parts.append(metadata['title'])
        if metadata.get('subject'):
            parts.append(metadata['subject'])
        if metadata.get('key_terms'):
            parts.extend(metadata['key_terms'][:10])
        if metadata.get('entities'):
            parts.extend(metadata['entities'][:10])
        
        return ' '.join(parts)

