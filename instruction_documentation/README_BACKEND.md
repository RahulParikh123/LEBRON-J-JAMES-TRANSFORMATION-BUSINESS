# Backend API Documentation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Run the API Server

```bash
cd backend
python app.py
```

Or using uvicorn directly:
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### POST `/api/v1/process`

Upload and process a data file.

**Request:**
- `file` (multipart/form-data): Data file to process
- `narration` (optional): Human narration file
- `config` (optional): JSON configuration string

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "processing",
  "message": "File uploaded and processing started"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/process" \
  -F "file=@data.csv" \
  -F "narration=@narration.txt"
```

### GET `/api/v1/jobs/{job_id}`

Get the status of a processing job.

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "completed",
  "progress": 100.0,
  "message": "Processing completed successfully",
  "output_path": "/path/to/output.jsonl",
  "stats": {
    "entities_detected": 5,
    "entities_redacted": 5,
    "output_records": 10
  }
}
```

### GET `/api/v1/jobs/{job_id}/download`

Download the processed result file.

**Response:** File download (JSONL format)

### GET `/api/v1/jobs`

List recent jobs.

**Query Parameters:**
- `limit` (optional): Number of jobs to return (default: 10)

### DELETE `/api/v1/jobs/{job_id}`

Delete a job and its associated files.

### GET `/api/v1/formats`

Get list of supported file formats.

**Response:**
```json
{
  "supported_formats": [".xlsx", ".csv", ".json", ".pptx"],
  "handlers": ["ExcelHandler", "CSVHandler", ...]
}
```

### GET `/health`

Health check endpoint.

## Usage Examples

### Python Client

```python
import requests
import time

# Upload file
with open('data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/v1/process', files=files)
    job_id = response.json()['job_id']

# Check status
while True:
    status = requests.get(f'http://localhost:8000/api/v1/jobs/{job_id}').json()
    if status['status'] == 'completed':
        break
    time.sleep(2)

# Download result
result = requests.get(f'http://localhost:8000/api/v1/jobs/{job_id}/download')
with open('output.jsonl', 'wb') as f:
    f.write(result.content)
```

### JavaScript/TypeScript Client

```typescript
async function processFile(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  
  // Upload
  const uploadResponse = await fetch('http://localhost:8000/api/v1/process', {
    method: 'POST',
    body: formData
  });
  const { job_id } = await uploadResponse.json();
  
  // Poll for completion
  while (true) {
    const statusResponse = await fetch(`http://localhost:8000/api/v1/jobs/${job_id}`);
    const status = await statusResponse.json();
    
    if (status.status === 'completed') {
      // Download result
      const resultResponse = await fetch(`http://localhost:8000/api/v1/jobs/${job_id}/download`);
      const blob = await resultResponse.blob();
      return blob;
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## Testing

Run the test script:
```bash
python test_api.py
```

Make sure the API server is running first!

