# Deployment Guide

This guide explains how to deploy the Data Transformation Platform as a backend service.

## Deployment Options

### Option 1: Local Development Server

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm

# Run the API server
cd backend
python app.py
```

The API will be available at `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Option 2: Docker Deployment

**Build and Run:**
```bash
# Build the Docker image
docker build -t data-transformation-platform .

# Run the container
docker run -p 8000:8000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/api_output:/app/api_output data-transformation-platform
```

**Using Docker Compose:**
```bash
docker-compose up -d
```

### Option 3: Cloud Deployment

#### AWS (EC2/ECS/Lambda)

**EC2 Deployment:**
1. Launch an EC2 instance (Ubuntu 22.04 LTS recommended)
2. Install Docker:
   ```bash
   sudo apt-get update
   sudo apt-get install docker.io docker-compose
   ```
3. Clone your repository
4. Run with Docker Compose

**ECS Deployment:**
1. Push Docker image to ECR
2. Create ECS task definition
3. Deploy to ECS cluster

**Lambda Deployment:**
- Use AWS SAM or Serverless Framework
- Package as Lambda layer (note: size limits apply)

#### Google Cloud Platform

**Cloud Run:**
```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/data-transformation-platform

# Deploy to Cloud Run
gcloud run deploy data-transformation-platform \
  --image gcr.io/PROJECT_ID/data-transformation-platform \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure

**Container Instances:**
```bash
# Build and push to ACR
az acr build --registry REGISTRY_NAME --image data-transformation-platform .

# Deploy to Container Instances
az container create \
  --resource-group RESOURCE_GROUP \
  --name data-transformation-platform \
  --image REGISTRY_NAME.azurecr.io/data-transformation-platform \
  --ports 8000 \
  --cpu 2 \
  --memory 4
```

## API Usage Examples

### Upload and Process File

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/process" \
  -F "file=@data.csv" \
  -F "narration=@narration.txt"
```

**Using Python:**
```python
import requests

files = {
    'file': open('data.csv', 'rb'),
    'narration': open('narration.txt', 'rb')
}

response = requests.post('http://localhost:8000/api/v1/process', files=files)
job_id = response.json()['job_id']
print(f"Job ID: {job_id}")
```

**Using JavaScript:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('narration', narrationFile);

fetch('http://localhost:8000/api/v1/process', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log('Job ID:', data.job_id));
```

### Check Job Status

```bash
curl "http://localhost:8000/api/v1/jobs/{job_id}"
```

### Download Result

```bash
curl "http://localhost:8000/api/v1/jobs/{job_id}/download" -o processed_data.jsonl
```

## Configuration

### Environment Variables

Create a `.env` file:
```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Storage
UPLOAD_DIR=./uploads
OUTPUT_DIR=./api_output

# Security (for production)
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
API_KEY=your-secret-api-key
```

### Production Settings

1. **Security:**
   - Enable authentication (API keys, OAuth, etc.)
   - Configure CORS properly
   - Use HTTPS
   - Implement rate limiting

2. **Storage:**
   - Use cloud storage (S3, Azure Blob, GCS) for uploads/outputs
   - Implement cleanup jobs for old files
   - Set up backup strategies

3. **Monitoring:**
   - Add logging (ELK, CloudWatch, etc.)
   - Set up health checks
   - Monitor resource usage
   - Track API metrics

4. **Scaling:**
   - Use load balancer for multiple instances
   - Implement job queue (Redis, RabbitMQ)
   - Use distributed storage
   - Consider serverless for cost optimization

## Saving the Model/Platform

### Option 1: Git Repository

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Data Transformation Platform"

# Push to GitHub/GitLab
git remote add origin https://github.com/yourusername/data-transformation-platform.git
git push -u origin main
```

### Option 2: Docker Image Registry

```bash
# Build and tag
docker build -t your-registry/data-transformation-platform:latest .

# Push to registry
docker push your-registry/data-transformation-platform:latest
```

### Option 3: Package as Python Library

```bash
# Build package
python setup.py sdist bdist_wheel

# Upload to PyPI (or private repository)
twine upload dist/*
```

## Maintenance

### Backup Strategy

1. **Code:** Use Git version control
2. **Data:** Regular backups of uploads/outputs
3. **Configuration:** Version control config files
4. **Database:** If using job tracking DB, regular backups

### Updates

1. Pull latest code
2. Update dependencies: `pip install -r requirements.txt --upgrade`
3. Rebuild Docker image if using containers
4. Restart services

### Monitoring

- Set up health check endpoints
- Monitor disk space (uploads/outputs)
- Track API response times
- Monitor error rates
- Set up alerts for failures

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Find and kill process
   lsof -ti:8000 | xargs kill -9
   ```

2. **Memory issues with large files:**
   - Increase container memory
   - Process files in batches
   - Use streaming for large files

3. **spaCy model not found:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Permission errors:**
   ```bash
   chmod -R 755 uploads api_output output
   ```

## Next Steps

1. Set up CI/CD pipeline
2. Add authentication/authorization
3. Implement job queue for better scalability
4. Add monitoring and alerting
5. Set up automated backups
6. Create frontend dashboard (optional)

