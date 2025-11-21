# Quick Start - Enterprise Scale Processing

## 🚀 Ready to Process Everything!

Your platform now supports **30+ file types** and **10+ enterprise systems**!

## Step 1: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Optional: For better PDF extraction
pip install pdfplumber

# Optional: For image OCR
pip install pytesseract
```

## Step 2: Run Batch Processing

```bash
# Process any directory - auto-detects ALL file types!
python test_batch.py --dir "YOUR_DATA_FOLDER"
```

**That's it!** The system will:
- ✅ Auto-detect file types (PDF, Excel, Word, images, etc.)
- ✅ Process all files in parallel
- ✅ Extract metadata and relationships
- ✅ Generate training data

---

## 📁 Supported File Types (Auto-Detected)

### Documents
- PDF, Word, PowerPoint, Excel, Markdown, Text

### Data Files
- CSV, JSON, XML, YAML, TOML, INI

### Images
- PNG, JPG, GIF, BMP, TIFF, WEBP, SVG

### Archives
- ZIP, TAR, GZ

### Databases
- PostgreSQL, MySQL, SQL Server, SQLite, Oracle, MongoDB

---

## 🏢 Enterprise Systems

### CRM Systems
- **Salesforce**: `salesforce://user:pass@instance.salesforce.com`
- **HubSpot**: `hubspot://api_key`
- **Dynamics**: `dynamics://instance.crm.dynamics.com`

### ERP Systems
- **SAP**: `sap://host:port`
- **Oracle ERP**: `oracleerp://host:port`
- **NetSuite**: `netsuite://account_id`

### Cloud Storage
- **OneDrive/SharePoint**: `onedrive://tenant_id`
- **Google Drive**: `googledrive://project_id`

---

## 💡 Example: Process Everything from a Company

```python
from main import DataTransformationPipeline

pipeline = DataTransformationPipeline()

# 1. Process all files in a directory
results = pipeline.process_batch(
    input_directory="acquired_company_data",
    output_directory="output",
    detect_relationships=True
)

# 2. Connect to their Salesforce
salesforce_data = pipeline.process(
    input_path="salesforce://user:pass@instance.salesforce.com",
    output_path="output/salesforce.jsonl"
)

# 3. Connect to their database
db_data = pipeline.process(
    input_path="postgresql://user:pass@host:5432/dbname",
    output_path="output/database.jsonl"
)

# 4. Process OneDrive files
onedrive_data = pipeline.process(
    input_path="onedrive://tenant_id",
    output_path="output/onedrive.jsonl"
)
```

---

## 📊 Output Structure

```
output/
├── processed/              # Individual processed files
│   ├── document1_processed.jsonl
│   ├── spreadsheet1_processed.jsonl
│   └── ...
├── relationships/          # File relationships
│   └── relationship_graph.json
├── metadata/               # File metadata index
│   └── file_metadata.json
└── agentic_ai/            # Training data
    └── training_data.jsonl
```

---

## ⚙️ Configuration

### For Enterprise Systems

Create `.env` file:
```bash
SALESFORCE_USERNAME=user@company.com
SALESFORCE_PASSWORD=password
HUBSPOT_API_KEY=your_key
MS_TENANT_ID=your_tenant
```

### Config File (`config.yaml`):
```yaml
enterprise_connectors:
  salesforce:
    enabled: true
    username: ${SALESFORCE_USERNAME}
    password: ${SALESFORCE_PASSWORD}
  
  hubspot:
    enabled: true
    api_key: ${HUBSPOT_API_KEY}
```

---

## 🎯 What Happens When You Run It

1. **File Scanning**: Finds all files in directory
2. **Type Detection**: Auto-detects file types
3. **Parallel Processing**: Processes files simultaneously
4. **Data Extraction**: Extracts structured data + text
5. **Metadata Extraction**: Author, dates, entities, key terms
6. **Relationship Detection**: Finds connections between files
7. **Training Data**: Generates LLM-ready training data

---

## 📈 Scalability

- ✅ **100+ files**: Handles easily
- ✅ **500GB+**: Processes in batches
- ✅ **Parallel processing**: Uses all CPU cores
- ✅ **Resume capability**: Can resume if interrupted
- ✅ **Error handling**: Continues on individual file errors

---

## 🔍 Check Results

```bash
# View summary
cat output/summary.json

# View relationships
cat output/relationships/relationship_graph.json

# View training data
head -n 5 output/agentic_ai/training_data.jsonl
```

---

## 🎉 You're Ready!

Just run:
```bash
python test_batch.py --dir "YOUR_DATA"
```

**All file types and enterprise systems are automatically detected and processed!**

