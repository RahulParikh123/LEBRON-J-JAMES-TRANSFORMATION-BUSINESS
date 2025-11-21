"""
Compliance rules for various regulations
"""
from typing import Dict, List, Any, Optional
import re


class ComplianceRules:
    """Define compliance rules for different regulations"""
    
    # GDPR (General Data Protection Regulation)
    GDPR_SENSITIVE_FIELDS = [
        'name', 'email', 'phone', 'address', 'ssn', 'passport',
        'credit_card', 'bank_account', 'ip_address', 'location',
        'biometric', 'genetic', 'health', 'sexual_orientation',
        'political', 'religious', 'ethnic'
    ]
    
    # HIPAA (Health Insurance Portability and Accountability Act)
    HIPAA_PHI_FIELDS = [
        'patient_name', 'medical_record', 'diagnosis', 'treatment',
        'prescription', 'lab_result', 'insurance', 'admission_date',
        'discharge_date', 'physician', 'hospital', 'procedure'
    ]
    
    # PCI DSS (Payment Card Industry Data Security Standard)
    PCI_SENSITIVE_FIELDS = [
        'card_number', 'cvv', 'expiry', 'cardholder_name',
        'track_data', 'pin', 'authentication_data'
    ]
    
    # SOX (Sarbanes-Oxley Act) - Financial data
    SOX_SENSITIVE_FIELDS = [
        'financial_statement', 'audit', 'internal_control',
        'revenue', 'expense', 'asset', 'liability', 'equity'
    ]
    
    def __init__(self):
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict[str, Dict]:
        """Load compliance rules"""
        return {
            'GDPR': {
                'name': 'General Data Protection Regulation',
                'sensitive_fields': self.GDPR_SENSITIVE_FIELDS,
                'requirements': [
                    'right_to_erasure',
                    'data_minimization',
                    'purpose_limitation',
                    'storage_limitation',
                    'consent_management'
                ],
                'check_function': self._check_gdpr
            },
            'HIPAA': {
                'name': 'Health Insurance Portability and Accountability Act',
                'sensitive_fields': self.HIPAA_PHI_FIELDS,
                'requirements': [
                    'phi_protection',
                    'access_controls',
                    'audit_logs',
                    'encryption',
                    'minimum_necessary'
                ],
                'check_function': self._check_hipaa
            },
            'PCI_DSS': {
                'name': 'Payment Card Industry Data Security Standard',
                'sensitive_fields': self.PCI_SENSITIVE_FIELDS,
                'requirements': [
                    'card_data_protection',
                    'encryption',
                    'access_controls',
                    'network_security',
                    'monitoring'
                ],
                'check_function': self._check_pci
            },
            'SOX': {
                'name': 'Sarbanes-Oxley Act',
                'sensitive_fields': self.SOX_SENSITIVE_FIELDS,
                'requirements': [
                    'financial_accuracy',
                    'internal_controls',
                    'audit_trail',
                    'data_retention'
                ],
                'check_function': self._check_sox
            }
        }
    
    def get_rule(self, regulation: str) -> Optional[Dict]:
        """Get rules for a specific regulation"""
        return self.rules.get(regulation.upper())
    
    def get_all_regulations(self) -> List[str]:
        """Get list of all supported regulations"""
        return list(self.rules.keys())
    
    def _check_gdpr(self, data_info: Dict, detected_entities: List[Dict]) -> Dict[str, Any]:
        """Check GDPR compliance"""
        issues = []
        
        # Check for sensitive personal data
        sensitive_detected = [e for e in detected_entities 
                            if e['type'].lower() in [f.lower() for f in self.GDPR_SENSITIVE_FIELDS]]
        
        if sensitive_detected:
            issues.append({
                'type': 'sensitive_data_detected',
                'severity': 'high',
                'message': f'GDPR-sensitive data detected: {len(sensitive_detected)} entities',
                'entities': sensitive_detected[:10]  # Limit to first 10
            })
        
        # Check for data minimization (excessive data collection)
        if data_info.get('column_count', 0) > 50:
            issues.append({
                'type': 'data_minimization',
                'severity': 'medium',
                'message': 'Large number of columns may violate data minimization principle'
            })
        
        return {
            'compliant': len(issues) == 0,
            'issues': issues,
            'recommendations': [
                'Implement data minimization',
                'Ensure consent management',
                'Provide right to erasure capability',
                'Limit data retention period'
            ]
        }
    
    def _check_hipaa(self, data_info: Dict, detected_entities: List[Dict]) -> Dict[str, Any]:
        """Check HIPAA compliance"""
        issues = []
        
        # Check for PHI
        phi_detected = [e for e in detected_entities 
                       if any(phi_field in e.get('type', '').lower() 
                             for phi_field in self.HIPAA_PHI_FIELDS)]
        
        if phi_detected:
            issues.append({
                'type': 'phi_detected',
                'severity': 'critical',
                'message': f'PHI detected: {len(phi_detected)} entities',
                'entities': phi_detected[:10]
            })
        
        # Check for proper de-identification
        if data_info.get('has_identifiers', False):
            issues.append({
                'type': 'identifiers_present',
                'severity': 'high',
                'message': 'Direct identifiers may be present in data'
            })
        
        return {
            'compliant': len(issues) == 0,
            'issues': issues,
            'recommendations': [
                'De-identify all PHI',
                'Implement access controls',
                'Maintain audit logs',
                'Encrypt data at rest and in transit',
                'Apply minimum necessary standard'
            ]
        }
    
    def _check_pci(self, data_info: Dict, detected_entities: List[Dict]) -> Dict[str, Any]:
        """Check PCI DSS compliance"""
        issues = []
        
        # Check for card data
        card_data = [e for e in detected_entities 
                    if 'CREDIT_CARD' in e.get('type', '') or 'CARD' in e.get('type', '')]
        
        if card_data:
            issues.append({
                'type': 'card_data_detected',
                'severity': 'critical',
                'message': f'Payment card data detected: {len(card_data)} entities',
                'entities': card_data[:10]
            })
        
        return {
            'compliant': len(issues) == 0,
            'issues': issues,
            'recommendations': [
                'Never store full card numbers',
                'Encrypt card data if storage is necessary',
                'Implement strong access controls',
                'Maintain secure network',
                'Regular security testing'
            ]
        }
    
    def _check_sox(self, data_info: Dict, detected_entities: List[Dict]) -> Dict[str, Any]:
        """Check SOX compliance"""
        issues = []
        
        # Check for financial data integrity
        if not data_info.get('has_audit_trail', False):
            issues.append({
                'type': 'missing_audit_trail',
                'severity': 'high',
                'message': 'Financial data should have audit trail'
            })
        
        # Check for data retention
        if not data_info.get('retention_policy', False):
            issues.append({
                'type': 'missing_retention_policy',
                'severity': 'medium',
                'message': 'Financial records should have retention policy'
            })
        
        return {
            'compliant': len(issues) == 0,
            'issues': issues,
            'recommendations': [
                'Maintain complete audit trail',
                'Implement data retention policies',
                'Ensure data accuracy and integrity',
                'Document internal controls'
            ]
        }

