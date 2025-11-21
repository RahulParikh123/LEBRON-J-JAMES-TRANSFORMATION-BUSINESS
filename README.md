# LEBRON-J'JAMES-TRANSFORMATION-BUSINESS

**Enterprise-Scale Data Transformation Platform for LLM Training**

A comprehensive, production-ready platform that transforms enterprise data from multiple sources (files, databases, CRM, ERP, cloud storage) into LLM-training-ready formats with intelligent relationship detection and agentic AI formatting.

---

## 🎯 Overview

This platform processes enterprise data at scale (100+ files, 500GB+ capacity) through a complete transformation pipeline:

1. **Ingestion** - Extract data from 40+ file types and enterprise systems
2. **Cleaning** - Normalize, deduplicate, and validate data
3. **Redaction** - Detect and redact PII/PHI
4. **Compliance** - Validate against GDPR, HIPAA, PCI-DSS, SOX
5. **Relationship Detection** - Intelligently link related files across systems
6. **Agentic AI Formatting** - Generate multi-file context training data

---

## ✨ Key Features

### 📁 **40+ File Type Support**
- **Documents**: PDF, Word, PowerPoint, Excel, Markdown, Text
- **Data**: CSV, JSON, XML, YAML, TOML, INI
- **Images**: PNG, JPG, GIF, BMP, TIFF, WEBP, SVG (with OCR)
- **Archives**: ZIP, TAR, GZIP

### 🗄️ **Enterprise System Connectors**
- **Databases**: PostgreSQL, MySQL, SQL Server, SQLite, Oracle, MongoDB
- **CRM**: Salesforce, HubSpot, Microsoft Dynamics
- **ERP**: SAP, Oracle ERP, NetSuite
- **Cloud**: OneDrive/SharePoint, Google Drive

### 🤖 **Intelligent Features**
- **Batch Processing**: Parallel processing of 100+ files
- **Relationship Detection**: Content-based, filename, and metadata matching
- **Multi-File Context**: Links related files (e.g., Excel → PowerPoint → Word)
- **Agentic AI Training**: Generates training data with relationship awareness
- **Scalable**: Handles enterprise-scale datasets

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS.git
cd LEBRON-J-JAMES-TRANSFORMATION-BUSINESS

# Install dependencies
pip install -r requirements.txt

# Optional: For better PDF extraction
pip install pdfplumber

# Optional: For image OCR
pip install pytesseract
```

### Basic Usage

```bash
# Process a directory of files
python test_batch.py --dir "YOUR_DATA_FOLDER"
```

### Process Enterprise Systems

```python
from main import DataTransformationPipeline

pipeline = DataTransformationPipeline()

# Process database
result = pipeline.process(
    input_path="postgresql://user:pass@host:5432/dbname",
    output_path="output/db.jsonl"
)

# Process Salesforce
result = pipeline.process(
    input_path="salesforce://user:pass@instance.salesforce.com",
    output_path="output/salesforce.jsonl"
)
```

---

## 📊 Sample Data

The repository includes sample files from a real test run:

**Input Files:**
- `samples/East West Bancorp Model V2.xlsx` - Excel financial model
- `samples/Sherry_Hu_Resume.docx` - Word document
- `samples/FNP_ATZ_PJ_V2.pptx` - PowerPoint presentation

**Processed Outputs:**
- `samples/East West Bancorp Model V2_processed.jsonl`
- `samples/Sherry_Hu_Resume_processed.jsonl`
- `samples/FNP_ATZ_PJ_V2_processed.jsonl`

These demonstrate the complete transformation pipeline from raw files to LLM-ready training data.

---

## 📚 Documentation

### Quick Guides (Root)
- **[README.md](README.md)** - This file (overview and quick start)
- **[QUICK_START.md](QUICK_START.md)** - Getting started guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture overview

### Detailed Documentation (`/docs`)
- **[Technical Documentation](docs/TECHNICAL.md)** - Deep technical details
- **[Component Guide](docs/COMPONENTS.md)** - What each part of the codebase does
- **[API Reference](docs/API.md)** - API documentation
- **[Enterprise Connectors](docs/ENTERPRISE_CONNECTORS.md)** - Enterprise system integration
- **[Relationship Detection](docs/RELATIONSHIPS.md)** - How relationship detection works
- **[Agentic AI Formatting](docs/AGENTIC_AI.md)** - Training data generation

### Guides
- **[Batch Processing Guide](BATCH_PROCESSING_GUIDE.md)** - How to process multiple files
- **[Enterprise Connectors Guide](ENTERPRISE_CONNECTORS_GUIDE.md)** - Enterprise system setup
- **[How to Add Your Data](HOW_TO_ADD_YOUR_DATA.md)** - Data preparation guide

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Transformation Pipeline              │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌─────▼─────┐         ┌─────▼─────┐
   │Ingestion│          │  Cleaning │         │ Redaction  │
   │  Layer  │─────────▶│   Layer   │────────▶│   Layer   │
   └────┬────┘          └─────┬─────┘         └─────┬─────┘
        │                     │                     │
        │              ┌─────▼─────┐                │
        │              │Compliance │                │
        │              │   Layer   │                │
        │              └─────┬─────┘                │
        │                     │                     │
   ┌────▼─────────────────────┼─────────────────────▼────┐
   │            Relationship Detection                     │
   │  (Content-based, Filename, Metadata Matching)        │
   └─────────────────────┬─────────────────────────────────┘
                         │
   ┌─────────────────────▼─────────────────────────────────┐
   │         Agentic AI Formatting                         │
   │  (Multi-file context, Training data generation)      │
   └─────────────────────┬─────────────────────────────────┘
                         │
                  ┌──────▼──────┐
                  │   Output    │
                  │  (JSONL)    │
                  └─────────────┘
```

**Key Components:**
- **Ingestion**: 40+ file handlers + enterprise connectors
- **Processing**: Cleaning, redaction, compliance checking
- **Intelligence**: Relationship detection, metadata extraction
- **Output**: LLM-ready training data with multi-file context

---

## 📁 Project Structure

```
LEBRON-J-JAMES-TRANSFORMATION-BUSINESS/
├── src/
│   ├── ingestion/          # File format handlers
│   │   ├── excel_handler.py
│   │   ├── pdf_handler.py
│   │   ├── word_handler.py
│   │   ├── enterprise_connectors.py
│   │   └── ...
│   ├── cleaning/           # Data cleaning pipeline
│   ├── redaction/          # PII/PHI detection & redaction
│   ├── compliance/         # Regulatory compliance checking
│   ├── batch/              # Batch processing
│   ├── relationships/      # Relationship detection
│   └── structuring/        # LLM formatting
├── samples/                # Sample input/output files
├── docs/                   # Detailed documentation
├── main.py                 # Main pipeline orchestrator
├── test_batch.py           # Batch processing test script
└── requirements.txt        # Python dependencies
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```bash
# Salesforce
SALESFORCE_USERNAME=user@company.com
SALESFORCE_PASSWORD=password

# HubSpot
HUBSPOT_API_KEY=your_api_key

# Microsoft Graph (OneDrive)
MS_TENANT_ID=your_tenant_id
MS_CLIENT_ID=your_client_id
MS_CLIENT_SECRET=your_secret
```

### Config File (`config.yaml`)

```yaml
batch:
  max_workers: 4
  chunk_size: 100

relationships:
  min_confidence: 0.7
  strategies:
    - content
    - filename
    - metadata

redaction:
  strategy: mask
  entities: [EMAIL, PHONE, SSN]
```

---

## 📈 Performance

- **Throughput**: Processes 100+ files in parallel
- **Scale**: Handles 500GB+ datasets
- **Speed**: Parallel processing with progress tracking
- **Resume**: Can resume interrupted batch jobs
- **Error Handling**: Graceful error handling per file

---

## 🧪 Testing

```bash
# Run batch processing test
python test_batch.py --dir "test_data"

# Run single file test
python test_poc.py
```

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

This is a private enterprise project. For questions or contributions, please contact the repository owner.

---

## 📞 Support

For technical questions or issues:
1. Check the [documentation](docs/)
2. Review [sample files](samples/)
3. Contact the repository owner

---

## 🎯 Use Cases

- **Company Acquisitions**: Process all data from acquired companies
- **Data Migration**: Transform legacy data for modern systems
- **LLM Training**: Generate training data from enterprise documents
- **Compliance**: Ensure data meets regulatory requirements
- **Data Integration**: Unify data from multiple enterprise systems

---

## 🚀 Roadmap

- [x] Batch processing (100+ files)
- [x] Relationship detection
- [x] Enterprise connectors
- [x] Agentic AI formatting
- [ ] Distributed processing (Dask/Spark)
- [ ] Web UI
- [ ] Real-time processing
- [ ] Advanced analytics

---

**Built for enterprise scale. Production ready.** 🚀
