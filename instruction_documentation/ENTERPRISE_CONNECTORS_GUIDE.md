# Enterprise Connectors & File Handlers Guide

## 🎉 What's Been Added

### ✅ File Type Handlers (20+ formats)

**Document Formats:**
- ✅ PDF (`.pdf`) - with table extraction
- ✅ Word (`.docx`, `.doc`) - paragraphs, tables
- ✅ PowerPoint (`.pptx`, `.ppt`) - slides, tables
- ✅ Excel (`.xlsx`, `.xls`, `.xlsm`) - all sheets
- ✅ Markdown (`.md`, `.markdown`) - formatted text
- ✅ Text (`.txt`, `.log`) - plain text

**Data Formats:**
- ✅ CSV (`.csv`) - delimited data
- ✅ JSON (`.json`) - structured data
- ✅ XML (`.xml`) - hierarchical data
- ✅ YAML (`.yaml`, `.yml`) - configuration
- ✅ TOML (`.toml`) - configuration
- ✅ INI (`.ini`, `.cfg`, `.conf`) - configuration

**Media Formats:**
- ✅ Images (`.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg`)
  - EXIF data extraction
  - OCR text extraction (optional)
  - Image metadata

**Archive Formats:**
- ✅ ZIP (`.zip`)
- ✅ TAR (`.tar`)
- ✅ GZIP (`.gz`)
- ✅ RAR (`.rar`) - requires rarfile
- ✅ 7Z (`.7z`) - requires py7zr

---

### ✅ Enterprise Database Connectors

**SQL Databases:**
- ✅ PostgreSQL
- ✅ MySQL
- ✅ SQL Server (MSSQL)
- ✅ SQLite
- ✅ Oracle
- ✅ MongoDB (NoSQL)

**Usage:**
```python
# Connection string format
postgresql://user:password@host:port/database
mysql://user:password@host:port/database
mssql://user:password@host:port/database
sqlite:///path/to/database.db
oracle://user:password@host:port/service
mongodb://user:password@host:port/database
```

---

### ✅ CRM System Connectors

**Salesforce:**
```python
# Connection string
salesforce://username:password@instance.salesforce.com

# Or use config
{
    "username": "user@example.com",
    "password": "password",
    "instance": "login.salesforce.com",
    "object_type": "Account"  # Account, Contact, Opportunity, etc.
}
```

**HubSpot:**
```python
# Connection string
hubspot://api_key

# Or use config
{
    "api_key": "your_api_key",
    "object_type": "contacts"  # contacts, companies, deals, etc.
}
```

**Microsoft Dynamics CRM:**
```python
# Connection string
dynamics://instance.crm.dynamics.com

# Or use config
{
    "instance": "yourinstance.crm.dynamics.com",
    "entity": "accounts"  # accounts, contacts, opportunities, etc.
}
```

---

### ✅ ERP System Connectors

**SAP:**
```python
# Connection string
sap://host:port

# Or use ODBC/RFC connection
{
    "host": "sap_server",
    "port": 8000,
    "table": "MARA"  # Material master, etc.
}
```

**Oracle ERP:**
```python
# Connection string
oracleerp://host:port

# Or use config
{
    "module": "Financials"  # Financials, Supply Chain, HR, etc.
}
```

**NetSuite:**
```python
# Connection string
netsuite://account_id

# Or use config
{
    "account_id": "your_account",
    "record_type": "customer"  # customer, vendor, item, etc.
}
```

---

### ✅ Cloud Storage Connectors

**Microsoft OneDrive/SharePoint:**
```python
# Connection string
onedrive://tenant_id

# Or use Microsoft Graph API
{
    "tenant_id": "your_tenant",
    "client_id": "your_client_id",
    "client_secret": "your_secret",
    "folder_path": "/Documents"
}
```

**Google Drive:**
```python
# Connection string
googledrive://project_id

# Or use Google API
{
    "credentials_path": "path/to/credentials.json",
    "folder_id": "folder_id_here"
}
```

---

## 🚀 How to Use

### 1. Install Dependencies

```bash
# Core dependencies (required)
pip install -r requirements.txt

# Optional: For PDF table extraction
pip install pdfplumber

# Optional: For image OCR
pip install pytesseract
# Also need Tesseract installed: https://github.com/tesseract-ocr/tesseract

# Optional: For enterprise connectors
pip install simple-salesforce  # Salesforce
pip install hubspot-api-client  # HubSpot
pip install msal  # Microsoft Graph (OneDrive)
pip install google-api-python-client  # Google Drive
```

### 2. Process Files

```bash
# Process any directory - auto-detects file types!
python test_batch.py --dir "YOUR_DATA_FOLDER"
```

The system will:
- ✅ Auto-detect file types
- ✅ Use appropriate handler
- ✅ Extract data and metadata
- ✅ Detect relationships
- ✅ Generate training data

### 3. Connect to Enterprise Systems

**For Database:**
```python
from main import DataTransformationPipeline

pipeline = DataTransformationPipeline()
result = pipeline.process(
    input_path="postgresql://user:pass@host:5432/dbname",
    output_path="output/db_data.jsonl"
)
```

**For CRM/ERP:**
```python
# Salesforce
result = pipeline.process(
    input_path="salesforce://user:pass@instance.salesforce.com",
    output_path="output/salesforce.jsonl"
)

# HubSpot
result = pipeline.process(
    input_path="hubspot://api_key",
    output_path="output/hubspot.jsonl"
)
```

---

## 📋 Supported File Types Summary

| Category | Formats | Handler |
|----------|---------|---------|
| **Documents** | PDF, Word, PowerPoint, Excel | ✅ All |
| **Data** | CSV, JSON, XML, YAML, TOML, INI | ✅ All |
| **Text** | TXT, MD, LOG | ✅ All |
| **Images** | PNG, JPG, GIF, BMP, TIFF, WEBP, SVG | ✅ All |
| **Archives** | ZIP, TAR, GZ | ✅ All |
| **Databases** | PostgreSQL, MySQL, SQL Server, SQLite, Oracle, MongoDB | ✅ All |
| **CRM** | Salesforce, HubSpot, Dynamics | ✅ All |
| **ERP** | SAP, Oracle ERP, NetSuite | ✅ All |
| **Cloud** | OneDrive, SharePoint, Google Drive | ✅ All |

---

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```bash
# Salesforce
SALESFORCE_USERNAME=user@example.com
SALESFORCE_PASSWORD=password
SALESFORCE_INSTANCE=login.salesforce.com

# HubSpot
HUBSPOT_API_KEY=your_api_key

# Microsoft Graph (OneDrive)
MS_TENANT_ID=your_tenant_id
MS_CLIENT_ID=your_client_id
MS_CLIENT_SECRET=your_secret

# Google Drive
GOOGLE_CREDENTIALS_PATH=path/to/credentials.json
```

### Config File

```yaml
enterprise_connectors:
  salesforce:
    enabled: true
    username: ${SALESFORCE_USERNAME}
    password: ${SALESFORCE_PASSWORD}
  
  hubspot:
    enabled: true
    api_key: ${HUBSPOT_API_KEY}
  
  onedrive:
    enabled: true
    tenant_id: ${MS_TENANT_ID}
    client_id: ${MS_CLIENT_ID}
```

---

## ⚠️ Important Notes

### Mock Data Mode
Enterprise connectors return **mock data structures** by default. To get real data:
1. Install the appropriate API client library
2. Configure credentials (API keys, OAuth, etc.)
3. The handler will automatically use real API calls

### Scalability
- All handlers are designed for batch processing
- Database connectors support large result sets
- Cloud storage connectors can process entire folders
- File handlers process files in parallel

### Security
- Never commit credentials to version control
- Use environment variables or secure config files
- Enterprise connectors require proper authentication
- Database connections should use encrypted connections

---

## 🎯 Next Steps

1. **Test with your files:**
   ```bash
   python test_batch.py --dir "YOUR_DATA"
   ```

2. **Configure enterprise systems:**
   - Set up API credentials
   - Test connections
   - Process data

3. **Scale up:**
   - Process 100+ files
   - Connect to multiple systems
   - Generate training data

---

**All handlers are registered automatically!** Just run the batch processor and it will detect and process any supported file type or system connection.

