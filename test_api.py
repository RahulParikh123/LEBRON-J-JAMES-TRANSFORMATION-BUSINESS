"""
Test script for the API backend
"""
import requests
import time
import json
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_upload_and_process():
    """Test file upload and processing"""
    print("Testing file upload and processing...")
    
    # Create a test file
    test_data = {
        'name': ['John Doe', 'Jane Smith'],
        'email': ['john@example.com', 'jane@example.com'],
        'age': [30, 25]
    }
    
    import pandas as pd
    df = pd.DataFrame(test_data)
    test_file = 'test_upload.csv'
    df.to_csv(test_file, index=False)
    
    # Upload file
    with open(test_file, 'rb') as f:
        files = {'file': (test_file, f, 'text/csv')}
        response = requests.post(f"{API_BASE_URL}/api/v1/process", files=files)
    
    if response.status_code == 200:
        job_id = response.json()['job_id']
        print(f"✓ File uploaded. Job ID: {job_id}")
        
        # Poll for status
        print("Waiting for processing...")
        max_wait = 60  # seconds
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status_response = requests.get(f"{API_BASE_URL}/api/v1/jobs/{job_id}")
            status = status_response.json()
            
            print(f"  Status: {status['status']}, Progress: {status['progress']}%")
            
            if status['status'] == 'completed':
                print(f"✓ Processing completed!")
                print(f"  Stats: {json.dumps(status.get('stats', {}), indent=2)}")
                
                # Download result
                download_response = requests.get(f"{API_BASE_URL}/api/v1/jobs/{job_id}/download")
                if download_response.status_code == 200:
                    output_file = f"downloaded_{job_id}.jsonl"
                    with open(output_file, 'wb') as f:
                        f.write(download_response.content)
                    print(f"✓ Result downloaded to {output_file}")
                
                break
            elif status['status'] == 'failed':
                print(f"✗ Processing failed: {status.get('error', 'Unknown error')}")
                break
            
            time.sleep(2)
        else:
            print("✗ Timeout waiting for processing")
    else:
        print(f"✗ Upload failed: {response.status_code}")
        print(response.text)
    
    # Cleanup
    Path(test_file).unlink()
    print()


def test_supported_formats():
    """Test supported formats endpoint"""
    print("Testing supported formats endpoint...")
    response = requests.get(f"{API_BASE_URL}/api/v1/formats")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Supported formats: {data['supported_formats']}")
        print(f"✓ Handlers: {data['handlers']}")
    print()


def main():
    """Run all API tests"""
    print("="*60)
    print("API Backend Test Suite")
    print("="*60 + "\n")
    
    print("Make sure the API server is running:")
    print("  cd backend && python app.py\n")
    
    try:
        test_health()
        test_supported_formats()
        test_upload_and_process()
        
        print("="*60)
        print("✓ All tests completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to API server.")
        print("  Make sure the server is running at http://localhost:8000")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

