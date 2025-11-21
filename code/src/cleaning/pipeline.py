"""
Data cleaning pipeline - orchestrates normalization, deduplication, validation
"""
from typing import Any, Dict, List, Optional
import pandas as pd
from .normalizer import DataNormalizer
from .deduplicator import DataDeduplicator
from .validator import DataValidator


class CleaningPipeline:
    """Orchestrates the data cleaning process"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.normalizer = DataNormalizer(self.config.get('normalization', {}))
        self.deduplicator = DataDeduplicator(self.config.get('deduplication', {}))
        self.validator = DataValidator(self.config.get('validation', {}))
    
    def clean(self, data: Any, schema: Optional[Dict] = None, 
              key_columns: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run complete cleaning pipeline
        
        Args:
            data: Data to clean (DataFrame, list, or dict)
            schema: Optional validation schema
            key_columns: Columns to use for deduplication
        
        Returns:
            Dict with cleaned data and statistics
        """
        results = {
            'original_data': data,
            'steps': [],
            'stats': {}
        }
        
        current_data = data
        
        # Step 1: Normalize
        if self.config.get('normalize', True):
            norm_result = self.normalizer.normalize(current_data)
            current_data = norm_result['data']
            results['steps'].append({
                'step': 'normalization',
                'stats': norm_result.get('stats', {})
            })
        
        # Step 2: Validate (before deduplication to catch issues early)
        validation_result = None
        if self.config.get('validate', True):
            validation_result = self.validator.validate(current_data, schema)
            results['steps'].append({
                'step': 'validation',
                'result': validation_result
            })
        
        # Step 3: Deduplicate
        if self.config.get('deduplicate', True):
            dedup_result = self.deduplicator.deduplicate(current_data, key_columns)
            current_data = dedup_result['data']
            results['steps'].append({
                'step': 'deduplication',
                'stats': dedup_result.get('stats', {})
            })
        
        # Step 4: Final validation
        if self.config.get('validate', True) and validation_result:
            final_validation = self.validator.validate(current_data, schema)
            results['steps'].append({
                'step': 'final_validation',
                'result': final_validation
            })
        
        results['cleaned_data'] = current_data
        results['stats'] = self._aggregate_stats(results['steps'])
        
        return results
    
    def _aggregate_stats(self, steps: List[Dict]) -> Dict[str, Any]:
        """Aggregate statistics from all cleaning steps"""
        stats = {
            'total_steps': len(steps),
            'duplicates_removed': 0,
            'validation_issues': 0,
            'transformations_applied': []
        }
        
        for step in steps:
            if step['step'] == 'deduplication' and 'stats' in step:
                stats['duplicates_removed'] = step['stats'].get('total_duplicates_removed', 0)
            
            if step['step'] in ['validation', 'final_validation'] and 'result' in step:
                validation_result = step['result']
                if 'summary' in validation_result:
                    stats['validation_issues'] = validation_result['summary'].get('total_issues', 0)
            
            if step['step'] == 'normalization' and 'stats' in step:
                transformations = step['stats'].get('transformations', [])
                stats['transformations_applied'].extend(transformations)
        
        return stats

