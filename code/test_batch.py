"""
Easy test script for batch processing
"""
import sys
import argparse
from pathlib import Path
import json
from main import DataTransformationPipeline, load_config


def main():
    """Main test function"""
    parser = argparse.ArgumentParser(
        description='Test batch processing with your data files'
    )
    parser.add_argument(
        '--dir', '-d',
        help='Directory containing files to process',
        required=True
    )
    parser.add_argument(
        '--output', '-o',
        help='Output directory (default: output)',
        default='output'
    )
    parser.add_argument(
        '--no-relationships',
        action='store_true',
        help='Skip relationship detection'
    )
    parser.add_argument(
        '--config', '-c',
        help='Configuration file path'
    )
    
    args = parser.parse_args()
    
    # Check if directory exists
    input_dir = Path(args.dir)
    if not input_dir.exists():
        print(f"ERROR: Directory not found: {input_dir}")
        return 1
    
    if not input_dir.is_dir():
        print(f"ERROR: Path is not a directory: {input_dir}")
        return 1
    
    print("="*60)
    print("Enterprise Data Transformation Platform - Batch Test")
    print("="*60)
    print(f"\nInput directory: {input_dir}")
    print(f"Output directory: {args.output}")
    print(f"Relationship detection: {'Enabled' if not args.no_relationships else 'Disabled'}")
    print("\n" + "="*60)
    
    # Load configuration
    config = load_config(args.config)
    
    # Configure batch processing
    config.setdefault('batch', {})['max_workers'] = config.get('batch', {}).get('max_workers', 4)
    config.setdefault('batch', {})['resume'] = config.get('batch', {}).get('resume', True)
    
    # Configure relationships
    config.setdefault('relationships', {})['min_confidence'] = config.get('relationships', {}).get('min_confidence', 0.7)
    config.setdefault('relationships', {})['use_filename_strategy'] = True
    config.setdefault('relationships', {})['use_content_strategy'] = True
    config.setdefault('relationships', {})['use_metadata_strategy'] = True
    config.setdefault('relationships', {})['use_semantic_strategy'] = False  # Optional
    
    # Initialize pipeline
    print("\nInitializing pipeline...")
    pipeline = DataTransformationPipeline(config)
    
    # Process batch
    print("\nProcessing files...")
    try:
        results = pipeline.process_batch(
            input_directory=str(input_dir),
            output_directory=args.output,
            detect_relationships=not args.no_relationships
        )
        
        # Print results
        print("\n" + "="*60)
        print("BATCH PROCESSING COMPLETE!")
        print("="*60)
        print(f"\nFiles processed: {results.get('files_processed', 0)}")
        print(f"Relationships found: {results.get('relationships_found', 0)}")
        print(f"\nOutput directory: {results.get('output_directory', args.output)}")
        
        if results.get('relationship_graph'):
            print(f"\nRelationship graph: {results['relationship_graph']}")
        
        if results.get('agentic_ai_output'):
            print(f"Agentic AI training data: {results['agentic_ai_output']}")
        
        print("\n" + "="*60)
        print("Check the output directory for detailed results!")
        print("="*60)
        
        # Show summary file location
        summary_file = Path(args.output) / "summary.json"
        if summary_file.exists():
            print(f"\nSummary file: {summary_file}")
            print("\nQuick summary:")
            with open(summary_file, 'r') as f:
                summary = json.load(f)
                batch = summary.get('batch_results', {})
                print(f"  - Files found: {batch.get('files_found', 0)}")
                print(f"  - Files processed: {batch.get('files_processed', 0)}")
                print(f"  - Files failed: {batch.get('files_failed', 0)}")
                print(f"  - Progress: {batch.get('progress_percent', 0)}%")
        
        return 0
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

