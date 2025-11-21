# Quick Reference Guide

## 🚀 Quick Start

### Test the Platform (Proof of Concept)

```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 2. Run the test script
python test_poc.py
```

This will:
- Create sample data files (CSV, JSON, Excel)
- Process them through the pipeline
- Show you the results
- Generate training-ready JSONL files

### Run as Backend API

```bash
# 1. Install backend dependencies
pip install -r backend/requirements.txt

# 2. Start the API server
cd backend
python app.py

# 3. Access API docs
# Open browser: http://localhost:8000/docs
```

## 📦 How to Save/Deploy Your Platform

### Option 1: Save to Git Repository (Recommended)

```bash
# Initialize git
git init
git add .
git commit -m "Data Transformation Platform v0.1"

# Push to GitHub/GitLab
git remote add origin https://github.com/yourusername/data-transformation-platform.git
git push -u origin main
```

### Option 2: Save as Docker Image

```bash
# Build Docker image
docker build -t data-transformation-platform:latest .

# Save to file
docker save data-transformation-platform:latest -o data-transformation-platform.tar

# Load later
docker load -i data-transformation-platform.tar
```

### Option 3: Package for Distribution

```bash
# Create Python package
python setup.py sdist bdist_wheel

# Install from local package
pip install dist/data-transformation-platform-0.1.0.tar.gz
```

### Option 4: Deploy to Cloud

**AWS:**
```bash
# Push to ECR
aws ecr create-repository --repository-name data-transformation-platform
docker tag data-transformation-platform:latest YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/data-transformation-platform:latest
docker push YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/data-transformation-platform:latest
```

**Google Cloud:**
```bash
# Push to GCR
gcloud builds submit --tag gcr.io/PROJECT_ID/data-transformation-platform
```

**Azure:**
```bash
# Push to ACR
az acr build --registry REGISTRY_NAME --image data-transformation-platform .
```

## 📝 File Structure

```
data-transformation-platform/
├── src/                    # Core platform code
│   ├── ingestion/         # Format handlers
│   ├── cleaning/          # Data cleaning
│   ├── redaction/         # PII redaction
│   ├── compliance/        # Compliance checking
│   ├── structuring/      # LLM formatting
│   └── output/           # File writing
├── backend/               # FastAPI backend
│   ├── app.py            # API server
│   └── requirements.txt  # Backend deps
├── config/               # Configuration files
├── main.py               # CLI entry point
├── test_poc.py          # POC test script
├── test_api.py          # API test script
├── Dockerfile           # Docker config
├── docker-compose.yml    # Docker Compose
└── requirements.txt      # Python dependencies
```

## 🔧 Common Commands

### Process a File (CLI)
```bash
python main.py --input data.csv --output processed.jsonl --narration narration.txt
```

### Process with Config
```bash
python main.py --input data.xlsx --config config/example.yaml --output output.jsonl
```

### Start API Server
```bash
cd backend && python app.py
```

### Run with Docker
```bash
docker-compose up -d
```

### Test API
```bash
python test_api.py
```

## 📊 What Gets Generated

After processing, you'll get:

1. **Processed JSONL file** - Ready for LLM training
   - Contains structured data
   - Text representations
   - Human narration (if provided)
   - Metadata

2. **Processing statistics**
   - Entities detected/redacted
   - Duplicates removed
   - Compliance issues found
   - Record counts

3. **Compliance report**
   - GDPR/HIPAA/PCI-DSS checks
   - Issues and recommendations

## 🎯 Next Steps

1. **Test with your data:**
   - Upload your files
   - Run `test_poc.py` with your data
   - Review the output

2. **Deploy as backend:**
   - Start the API server
   - Integrate with your applications
   - Use the REST API

3. **Customize:**
   - Edit `config/example.yaml`
   - Add custom format handlers
   - Extend compliance rules

4. **Scale:**
   - Deploy to cloud
   - Use Docker containers
   - Set up load balancing

## 📚 Documentation

- **README.md** - Overview and features
- **QUICKSTART.md** - Getting started guide
- **ARCHITECTURE.md** - System architecture
- **DEPLOYMENT.md** - Deployment instructions
- **README_BACKEND.md** - API documentation

## 🆘 Troubleshooting

**Issue:** spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

**Issue:** Port 8000 already in use
```bash
# Change port in backend/app.py or use:
uvicorn backend.app:app --port 8001
```

**Issue:** Memory errors with large files
- Process in batches
- Increase Docker memory limits
- Use cloud storage for large files

## 💡 Tips

1. **For large datasets:** Use batch processing or cloud deployment
2. **For production:** Add authentication, rate limiting, monitoring
3. **For scalability:** Use job queues (Redis, RabbitMQ)
4. **For storage:** Use cloud storage (S3, Azure Blob, GCS)

