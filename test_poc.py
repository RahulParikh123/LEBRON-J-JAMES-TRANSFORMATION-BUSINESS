"""
Proof of Concept Test Script
Demonstrates the Data Transformation Platform with sample data
"""
import os
import json
import pandas as pd
from pathlib import Path
from main import DataTransformationPipeline

def create_sample_data():
    """Create sample data files for testing"""
    print("Creating sample data files...")
    
    # Create output directory
    os.makedirs('test_data', exist_ok=True)
    
    # 1. Sample CSV with PII
    print("  - Creating sample CSV...")
    csv_data = pd.DataFrame({
        'customer_id': [1, 2, 3, 4, 5],
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'John Doe', 'Alice Brown'],
        'email': ['john.doe@example.com', 'jane.smith@example.com', 'bob@example.com', 'john.doe@example.com', 'alice@example.com'],
        'phone': ['555-1234', '555-5678', '555-9012', '555-1234', '555-3456'],
        'ssn': ['123-45-6789', '987-65-4321', '456-78-9012', '123-45-6789', '789-01-2345'],
        'address': ['123 Main St', '456 Oak Ave', '789 Pine Rd', '123 Main St', '321 Elm St'],
        'age': [30, 25, 35, 30, 28],
        'purchase_amount': [99.99, 149.50, 79.99, 99.99, 199.99]
    })
    csv_data.to_csv('test_data/sample_customers.csv', index=False)
    
    # 2. Sample JSON data
    print("  - Creating sample JSON...")
    json_data = [
        {
            'product_id': 1,
            'product_name': 'Laptop Pro',
            'category': 'Electronics',
            'price': 1299.99,
            'description': 'High-performance laptop for professionals',
            'in_stock': True
        },
        {
            'product_id': 2,
            'product_name': 'Wireless Mouse',
            'category': 'Accessories',
            'price': 29.99,
            'description': 'Ergonomic wireless mouse',
            'in_stock': True
        },
        {
            'product_id': 3,
            'product_name': 'Mechanical Keyboard',
            'category': 'Accessories',
            'price': 149.99,
            'description': 'RGB mechanical keyboard',
            'in_stock': False
        }
    ]
    with open('test_data/sample_products.json', 'w') as f:
        json.dump(json_data, f, indent=2)
    
    # 3. Sample Excel file
    print("  - Creating sample Excel...")
    with pd.ExcelWriter('test_data/sample_sales.xlsx', engine='openpyxl') as writer:
        # Sheet 1: Sales data
        sales_data = pd.DataFrame({
            'sale_id': [1, 2, 3, 4, 5],
            'date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
            'customer_email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com', 'john@example.com'],
            'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Laptop'],
            'quantity': [1, 2, 1, 1, 1],
            'total': [1299.99, 59.98, 149.99, 299.99, 1299.99]
        })
        sales_data.to_excel(writer, sheet_name='Sales', index=False)
        
        # Sheet 2: Summary
        summary_data = pd.DataFrame({
            'metric': ['Total Sales', 'Average Order', 'Unique Customers', 'Top Product'],
            'value': [3109.94, 621.99, 4, 'Laptop']
        })
        summary_data.to_excel(writer, sheet_name='Summary', index=False)
    
    # 4. Sample narration file
    print("  - Creating sample narration...")
    narration = """
    This dataset contains customer information and sales data from our e-commerce platform.
    
    The customer data includes personal information such as names, email addresses, phone numbers,
    and social security numbers. This data has been collected over the past quarter and represents
    our active customer base.
    
    The sales data shows transaction details including dates, products purchased, quantities, and
    total amounts. We've identified that laptops are our top-selling product, with multiple repeat
    customers.
    
    Key insights:
    - Total sales: $3,109.94
    - Average order value: $621.99
    - 4 unique customers
    - Laptop is the top product
    
    This data will be used to train our recommendation system and improve customer segmentation.
    """
    with open('test_data/narration.txt', 'w') as f:
        f.write(narration)
    
    print("[OK] Sample data created successfully!\n")


def test_csv_processing():
    """Test CSV file processing"""
    print("="*60)
    print("TEST 1: Processing CSV File")
    print("="*60)
    
    pipeline = DataTransformationPipeline()
    
    results = pipeline.process(
        input_path='test_data/sample_customers.csv',
        output_path='test_output/customers_processed.jsonl',
        narration_path='test_data/narration.txt'
    )
    
    print(f"\n[OK] Status: {results['status']}")
    print(f"[OK] Output: {results['output_path']}")
    print(f"\nStatistics:")
    for key, value in results['stats'].items():
        print(f"  - {key}: {value}")
    
    # Show first few lines of output
    if Path(results['output_path']).exists():
        print(f"\nFirst 2 lines of output:")
        with open(results['output_path'], 'r') as f:
            for i, line in enumerate(f):
                if i >= 2:
                    break
                data = json.loads(line)
                print(f"  Record {i+1}:")
                print(f"    - ID: {data.get('id')}")
                print(f"    - Has structured data: {bool(data.get('structured_data'))}")
                print(f"    - Has text: {bool(data.get('text_representation'))}")
                print(f"    - Has narration: {bool(data.get('human_narration'))}")
    
    print("\n")


def test_json_processing():
    """Test JSON file processing"""
    print("="*60)
    print("TEST 2: Processing JSON File")
    print("="*60)
    
    pipeline = DataTransformationPipeline()
    
    results = pipeline.process(
        input_path='test_data/sample_products.json',
        output_path='test_output/products_processed.jsonl'
    )
    
    print(f"\n[OK] Status: {results['status']}")
    print(f"[OK] Output: {results['output_path']}")
    print(f"\nStatistics:")
    for key, value in results['stats'].items():
        print(f"  - {key}: {value}")
    print("\n")


def test_excel_processing():
    """Test Excel file processing"""
    print("="*60)
    print("TEST 3: Processing Excel File")
    print("="*60)
    
    pipeline = DataTransformationPipeline()
    
    results = pipeline.process(
        input_path='test_data/sample_sales.xlsx',
        output_path='test_output/sales_processed.jsonl',
        narration_path='test_data/narration.txt'
    )
    
    print(f"\n[OK] Status: {results['status']}")
    print(f"[OK] Output: {results['output_path']}")
    print(f"\nStatistics:")
    for key, value in results['stats'].items():
        print(f"  - {key}: {value}")
    print("\n")


def test_with_custom_config():
    """Test with custom configuration"""
    print("="*60)
    print("TEST 4: Processing with Custom Configuration")
    print("="*60)
    
    config = {
        'cleaning': {
            'deduplication': {
                'similarity_threshold': 0.9,
                'exact_match_only': False
            }
        },
        'redaction': {
            'redaction': {
                'strategy': 'mask',  # Mask PII instead of removing
                'entity_types': ['EMAIL', 'PHONE', 'SSN']
            }
        },
        'compliance': {
            'regulations': ['GDPR', 'HIPAA']
        },
        'llm_formatting': {
            'output_format': 'jsonl'
        },
        'log_level': 'INFO'
    }
    
    pipeline = DataTransformationPipeline(config)
    
    results = pipeline.process(
        input_path='test_data/sample_customers.csv',
        output_path='test_output/customers_custom_config.jsonl',
        narration_path='test_data/narration.txt'
    )
    
    print(f"\n[OK] Status: {results['status']}")
    print(f"[OK] Entities detected: {results['stats']['entities_detected']}")
    print(f"[OK] Entities redacted: {results['stats']['entities_redacted']}")
    print(f"[OK] Compliance issues: {results['stats']['compliance_issues']}")
    
    # Show compliance results
    for step in results['steps']:
        if step['step'] == 'compliance':
            compliance_result = step.get('result', {})
            print(f"\nCompliance Check Results:")
            print(f"  - Overall compliant: {compliance_result.get('overall_compliant', False)}")
            for reg, result in compliance_result.get('results', {}).items():
                print(f"  - {reg}: {'[OK] Compliant' if result.get('compliant') else '[X] Non-compliant'}")
                if result.get('issues'):
                    print(f"    Issues: {len(result['issues'])}")
    
    print("\n")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("Enterprise Data Transformation Platform - POC Test")
    print("="*60 + "\n")
    
    # Create directories
    os.makedirs('test_output', exist_ok=True)
    
    # Create sample data
    create_sample_data()
    
    # Run tests
    try:
        test_csv_processing()
        test_json_processing()
        test_excel_processing()
        test_with_custom_config()
        
        print("="*60)
        print("[OK] ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("\nOutput files are in the 'test_output' directory")
        print("Sample data files are in the 'test_data' directory")
        print("\nYou can now:")
        print("  1. Review the processed JSONL files")
        print("  2. Check the redaction results (PII should be masked)")
        print("  3. Verify compliance checking worked")
        print("  4. Use the output files for LLM training")
        
    except Exception as e:
        print(f"\n[X] Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

