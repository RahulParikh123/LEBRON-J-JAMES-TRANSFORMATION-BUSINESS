"""
Tool to view PII redaction information from processed files
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any, List


def load_processed_file(file_path: str) -> Dict[str, Any]:
    """Load a processed JSONL file"""
    records = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    record = json.loads(line)
                    # Parse the nested JSON in 'value' field
                    if 'value' in record:
                        value_str = record['value']
                        if isinstance(value_str, str):
                            value_data = json.loads(value_str)
                        else:
                            value_data = value_str
                        records.append(value_data)
                    else:
                        records.append(record)
                except json.JSONDecodeError:
                    continue
    return records


def extract_redaction_info(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract redaction information from records"""
    redaction_info = {
        'total_records': len(records),
        'records_with_redaction': 0,
        'total_entities_detected': 0,
        'total_entities_redacted': 0,
        'entity_summary': {},
        'detailed_redactions': []
    }
    
    for idx, record in enumerate(records):
        metadata = record.get('metadata', {})
        processing_stats = metadata.get('processing_stats', {})
        redaction_stats = processing_stats.get('redaction', {})
        
        entities_detected = redaction_stats.get('entities_detected', 0)
        entities_redacted = redaction_stats.get('entities_redacted', 0)
        entity_summary = redaction_stats.get('entity_summary', {})
        
        if entities_detected > 0 or entities_redacted > 0:
            redaction_info['records_with_redaction'] += 1
            redaction_info['total_entities_detected'] += entities_detected
            redaction_info['total_entities_redacted'] += entities_redacted
            
            # Merge entity summaries
            for entity_type, count in entity_summary.items():
                redaction_info['entity_summary'][entity_type] = \
                    redaction_info['entity_summary'].get(entity_type, 0) + count
            
            # Store detailed info
            redaction_info['detailed_redactions'].append({
                'record_index': idx,
                'record_id': record.get('id', f'record_{idx}'),
                'entities_detected': entities_detected,
                'entities_redacted': entities_redacted,
                'entity_types': list(entity_summary.keys()),
                'entity_summary': entity_summary
            })
    
    return redaction_info


def print_redaction_report(file_path: str):
    """Print a formatted redaction report"""
    print("=" * 80)
    print(f"PII REDACTION REPORT")
    print(f"File: {file_path}")
    print("=" * 80)
    print()
    
    try:
        records = load_processed_file(file_path)
        redaction_info = extract_redaction_info(records)
        
        # Summary
        print("SUMMARY")
        print("-" * 80)
        print(f"Total Records: {redaction_info['total_records']}")
        print(f"Records with PII Detected: {redaction_info['records_with_redaction']}")
        print(f"Total Entities Detected: {redaction_info['total_entities_detected']}")
        print(f"Total Entities Redacted: {redaction_info['total_entities_redacted']}")
        print()
        
        # Entity Summary
        if redaction_info['entity_summary']:
            print("ENTITY TYPES DETECTED")
            print("-" * 80)
            for entity_type, count in sorted(redaction_info['entity_summary'].items(), 
                                            key=lambda x: x[1], reverse=True):
                print(f"  {entity_type}: {count}")
            print()
        else:
            print("[OK] NO PII DETECTED")
            print("-" * 80)
            print("This file did not contain any detected PII/PHI.")
            print()
        
        # Detailed Redactions
        if redaction_info['detailed_redactions']:
            print("DETAILED REDACTIONS")
            print("-" * 80)
            for detail in redaction_info['detailed_redactions']:
                print(f"\nRecord {detail['record_index']} (ID: {detail['record_id']}):")
                print(f"  Entities Detected: {detail['entities_detected']}")
                print(f"  Entities Redacted: {detail['entities_redacted']}")
                if detail['entity_summary']:
                    print(f"  Entity Types:")
                    for entity_type, count in detail['entity_summary'].items():
                        print(f"    - {entity_type}: {count}")
        
        print()
        print("=" * 80)
        print("NOTE: Detailed location information (row, column, position)")
        print("      is available in the detection results but not saved")
        print("      to output files. To see exact locations, process with")
        print("      detect_only=True mode.")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] {str(e)}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python view_redaction_info.py <processed_file.jsonl>")
        print("\nExample:")
        print("  python view_redaction_info.py output/output/processed/Sherry_Hu_Resume_processed.jsonl")
        print("\nOr process all files in a directory:")
        print("  python view_redaction_info.py output/output/processed/")
        sys.exit(1)
    
    file_path = sys.argv[1]
    path = Path(file_path)
    
    if path.is_file():
        print_redaction_report(file_path)
    elif path.is_dir():
        # Process all JSONL files in directory
        jsonl_files = list(path.glob("*.jsonl"))
        if not jsonl_files:
            print(f"[ERROR] No JSONL files found in {file_path}")
            sys.exit(1)
        
        print(f"Found {len(jsonl_files)} processed files\n")
        for jsonl_file in sorted(jsonl_files):
            print_redaction_report(str(jsonl_file))
            print("\n" + "=" * 80 + "\n")
    else:
        print(f"[ERROR] Path not found: {file_path}")
        sys.exit(1)


if __name__ == '__main__':
    main()

