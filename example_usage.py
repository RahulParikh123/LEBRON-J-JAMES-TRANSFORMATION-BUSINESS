"""
Example usage of the Data Transformation Platform
"""
from main import DataTransformationPipeline
from pathlib import Path

# Example 1: Process a CSV file
def example_csv():
    print("Example 1: Processing CSV file")
    pipeline = DataTransformationPipeline()
    
    # Create sample CSV for demonstration
    import pandas as pd
    sample_data = pd.DataFrame({
        'name': ['John Doe', 'Jane Smith', 'John Doe'],
        'email': ['john@example.com', 'jane@example.com', 'john@example.com'],
        'phone': ['555-1234', '555-5678', '555-1234'],
        'age': [30, 25, 30]
    })
    sample_data.to_csv('sample_data.csv', index=False)
    
    results = pipeline.process(
        input_path='sample_data.csv',
        output_path='processed_sample.jsonl'
    )
    
    print(f"Status: {results['status']}")
    print(f"Output: {results['output_path']}")
    print(f"Records processed: {results['stats']['output_records']}")
    print()


# Example 2: Process with custom configuration
def example_with_config():
    print("Example 2: Processing with custom configuration")
    
    config = {
        'cleaning': {
            'deduplication': {
                'similarity_threshold': 0.9
            }
        },
        'redaction': {
            'redaction': {
                'strategy': 'mask',
                'entity_types': ['EMAIL', 'PHONE']
            }
        },
        'compliance': {
            'regulations': ['GDPR']
        },
        'llm_formatting': {
            'output_format': 'jsonl'
        }
    }
    
    pipeline = DataTransformationPipeline(config)
    
    # Process with narration
    narration = """
    This dataset contains customer information including names, 
    contact details, and demographic data. The data has been 
    cleaned and deduplicated to ensure quality.
    """
    
    # Save narration to file
    with open('narration.txt', 'w') as f:
        f.write(narration)
    
    results = pipeline.process(
        input_path='sample_data.csv',
        output_path='processed_with_narration.jsonl',
        narration_path='narration.txt'
    )
    
    print(f"Status: {results['status']}")
    print(f"Entities detected: {results['stats']['entities_detected']}")
    print(f"Entities redacted: {results['stats']['entities_redacted']}")
    print()


# Example 3: Process JSON data
def example_json():
    print("Example 3: Processing JSON file")
    
    import json
    
    # Create sample JSON
    sample_json = [
        {
            'id': 1,
            'name': 'Product A',
            'price': 99.99,
            'description': 'A great product'
        },
        {
            'id': 2,
            'name': 'Product B',
            'price': 149.99,
            'description': 'Another great product'
        }
    ]
    
    with open('sample_data.json', 'w') as f:
        json.dump(sample_json, f, indent=2)
    
    pipeline = DataTransformationPipeline()
    results = pipeline.process(
        input_path='sample_data.json',
        output_path='processed_json.jsonl'
    )
    
    print(f"Status: {results['status']}")
    print(f"Output: {results['output_path']}")
    print()


if __name__ == '__main__':
    print("="*60)
    print("Data Transformation Platform - Example Usage")
    print("="*60)
    print()
    
    try:
        example_csv()
        example_with_config()
        example_json()
        
        print("="*60)
        print("Examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

