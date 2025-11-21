"""
Compliance checker - validates data against regulations
"""
from typing import Any, Dict, List, Optional
import pandas as pd
from .rules import ComplianceRules


class ComplianceChecker:
    """Check data compliance with various regulations"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.rules = ComplianceRules()
        self.regulations_to_check = self.config.get('regulations', ['GDPR', 'HIPAA'])
    
    def check(self, data: Any, detected_entities: Optional[List[Dict]] = None,
              metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Check data compliance
        
        Args:
            data: Data to check
            detected_entities: Previously detected PII/PHI entities
            metadata: Additional metadata about the data
        
        Returns:
            Dict with compliance results
        """
        # Prepare data info
        data_info = self._extract_data_info(data, metadata)
        
        # Use provided entities or detect them
        if detected_entities is None:
            from ..redaction.pii_detector import PIIDetector
            detector = PIIDetector()
            detection_result = detector.detect(data)
            detected_entities = detection_result.get('entities', [])
        
        # Check each regulation
        results = {}
        overall_compliant = True
        
        for regulation in self.regulations_to_check:
            rule = self.rules.get_rule(regulation)
            if rule and rule.get('check_function'):
                check_result = rule['check_function'](data_info, detected_entities)
                results[regulation] = {
                    'name': rule['name'],
                    'compliant': check_result['compliant'],
                    'issues': check_result.get('issues', []),
                    'recommendations': check_result.get('recommendations', [])
                }
                
                if not check_result['compliant']:
                    overall_compliant = False
        
        return {
            'overall_compliant': overall_compliant,
            'regulations_checked': self.regulations_to_check,
            'results': results,
            'data_info': data_info,
            'summary': self._summarize_results(results)
        }
    
    def _extract_data_info(self, data: Any, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Extract information about the data"""
        info = {
            'has_identifiers': False,
            'has_audit_trail': False,
            'retention_policy': False,
            'column_count': 0,
            'row_count': 0
        }
        
        if isinstance(data, pd.DataFrame):
            info['column_count'] = len(data.columns)
            info['row_count'] = len(data)
            
            # Check for identifier columns
            id_keywords = ['id', 'identifier', 'key', 'uuid', 'guid']
            info['has_identifiers'] = any(
                any(keyword in str(col).lower() for keyword in id_keywords)
                for col in data.columns
            )
        
        if metadata:
            info.update(metadata)
        
        return info
    
    def _summarize_results(self, results: Dict[str, Dict]) -> Dict[str, Any]:
        """Summarize compliance check results"""
        total_issues = 0
        critical_issues = 0
        high_issues = 0
        
        for regulation, result in results.items():
            for issue in result.get('issues', []):
                total_issues += 1
                severity = issue.get('severity', 'medium')
                if severity == 'critical':
                    critical_issues += 1
                elif severity == 'high':
                    high_issues += 1
        
        return {
            'total_issues': total_issues,
            'critical_issues': critical_issues,
            'high_issues': high_issues,
            'compliant_regulations': sum(1 for r in results.values() if r['compliant']),
            'non_compliant_regulations': sum(1 for r in results.values() if not r['compliant'])
        }

