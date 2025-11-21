# Ingestion Layer - Code Summary

## Overview
The Ingestion Layer extracts data from diverse sources (files, databases, CRM, ERP, cloud storage) and converts it into a standardized format for processing.

---

## Key Components

### 1. Format Registry (`registry.py`)
**Purpose**: Central registry that manages all format handlers

**How it works**:
- Maintains a list of all available handlers (18 total)
- Auto-selects the appropriate handler for each file type
- Supports 40+ file formats and 10+ enterprise systems

**Key Methods**:
- `get_handler(file_path)`: Returns the handler that can process the file
- `get_supported_formats()`: Lists all supported file extensions
- `register(handler)`: Adds new handlers dynamically

---

### 2. Base Handler (`base_handler.py`)
**Purpose**: Abstract base class defining the interface for all handlers

**Key Features**:
- Standardizes data normalization (column names, types)
- Provides metadata extraction
- Ensures consistent output format across all handlers

**Output Format**:
```python
{
    'data': structured_data,      # DataFrame, list, or dict
    'metadata': file_metadata,    # File properties
    'text_content': [text],       # Human-readable text
    'structure': structure_info    # Format-specific structure
}
```

---

### 3. File Format Handlers

**Excel Handler** (`excel_handler.py`):
- Reads `.xlsx`, `.xls`, `.xlsm` files
- Extracts all sheets as separate data structures
- Converts to structured data + text representation
- Handles formulas, formatting, multiple sheets

**Word Handler** (`word_handler.py`):
- Reads `.docx` files
- Extracts paragraphs and tables
- Preserves document structure
- Converts to structured format

**PowerPoint Handler** (`ppt_handler.py`):
- Reads `.pptx` files
- Extracts slide content and tables
- Preserves slide structure
- Handles text, images, tables

**PDF Handler** (`pdf_handler.py`):
- Extracts text from PDFs
- Extracts tables (using pdfplumber)
- Handles multi-page documents
- Preserves document structure

**CSV/JSON/Text Handlers**:
- Standard data format handlers
- Handle encoding, delimiters, nested structures

**Image Handler** (`image_handler.py`):
- Reads images (PNG, JPG, etc.)
- Extracts EXIF metadata
- Optional OCR text extraction
- Provides image information

**Archive Handler** (`archive_handler.py`):
- Reads ZIP, TAR, GZIP files
- Lists files in archives
- Can extract files (optional)

---

### 4. Enterprise Connectors (`enterprise_connectors.py`)

**Database Connector** (`database_handler.py`):
- Connects to PostgreSQL, MySQL, SQL Server, SQLite, Oracle, MongoDB
- Executes queries or extracts entire tables
- Converts database data to structured format
- Handles large result sets

**CRM Connectors**:
- **Salesforce**: Connects via API, extracts objects (Account, Contact, etc.)
- **HubSpot**: Connects via API, extracts contacts, companies, deals
- **Dynamics**: Connects to Microsoft Dynamics CRM entities

**ERP Connectors**:
- **SAP**: Connects via ODBC/RFC, extracts tables/modules
- **Oracle ERP**: Connects to ERP modules (Financials, Supply Chain)
- **NetSuite**: Connects via API, extracts record types

**Cloud Storage Connectors**:
- **OneDrive/SharePoint**: Uses Microsoft Graph API
- **Google Drive**: Uses Google API
- Lists and extracts files from cloud storage

---

### 5. Metadata Extractor (`metadata_extractor.py`)
**Purpose**: Extracts rich metadata from files

**Extracts**:
- File properties (size, dates, author, title)
- Content signatures (hash, entities, key terms)
- Structure information (sheets, slides, sections)
- Document properties (EXIF, custom properties)

**Key Methods**:
- `extract(file_path)`: Extracts all metadata
- `to_dict(metadata)`: Converts to dictionary format

---

## Data Flow

```
Input File/System
    ↓
Format Detection (Registry)
    ↓
Handler Selection
    ↓
Data Extraction
    ├── Structured Data (DataFrame/list/dict)
    ├── Text Representation
    └── Metadata
    ↓
Standardized Output Format
```

---

## Supported Formats

**Files**: 20+ formats (Excel, Word, PowerPoint, PDF, CSV, JSON, XML, YAML, Images, Archives)
**Databases**: 6 types (PostgreSQL, MySQL, SQL Server, SQLite, Oracle, MongoDB)
**CRM**: 3 systems (Salesforce, HubSpot, Dynamics)
**ERP**: 3 systems (SAP, Oracle ERP, NetSuite)
**Cloud**: 2 systems (OneDrive, Google Drive)

**Total: 40+ formats and systems**

---

## Key Design Patterns

- **Strategy Pattern**: Different handlers for different formats
- **Factory Pattern**: Registry creates appropriate handlers
- **Template Method**: Base handler defines structure, subclasses implement specifics

---

## Output

All handlers produce consistent output:
- **Structured data**: Ready for processing
- **Text representation**: Human-readable version
- **Metadata**: File properties and content signatures
- **Structure**: Format-specific information (sheets, slides, etc.)

