# Component Guide

## What Each Part of the Codebase Does

This document explains what each component, module, and file in the codebase does.

---

## 📁 Directory Structure

```
LEBRON-J-JAMES-TRANSFORMATION-BUSINESS/
├── src/                          # Source code
│   ├── ingestion/                # Data ingestion layer
│   ├── cleaning/                 # Data cleaning layer
│   ├── redaction/                # PII/PHI redaction layer
│   ├── compliance/               # Regulatory compliance layer
│   ├── batch/                    # Batch processing
│   ├── relationships/            # Relationship detection
│   └── structuring/              # LLM formatting
├── samples/                      # Sample input/output files
├── docs/                         # Documentation
├── main.py                       # Main pipeline orchestrator
├── test_batch.py                 # Batch processing test script
└── requirements.txt              # Python dependencies
```

---

## 🎯 Core Files

### `main.py`
**Purpose**: Main entry point and pipeline orchestrator

**What it does**:
- Initializes the complete transformation pipeline
- Coordinates all processing steps
- Handles single file and batch processing
- Manages relationship detection
- Generates agentic AI training data

**Key Classes**:
- `DataTransformationPipeline`: Main pipeline class

**Key Methods**:
- `process()`: Process a single file
- `process_batch()`: Process directory with relationship detection

---

### `test_batch.py`
**Purpose**: Test script for batch processing

**What it does**:
- Provides easy command-line interface for batch processing
- Accepts directory path as argument
- Runs complete pipeline on all files in directory
- Shows progress and results

**Usage**:
```bash
python test_batch.py --dir "YOUR_DATA"
```

---

## 📥 Ingestion Layer (`src/ingestion/`)

**Purpose**: Extract data from various sources

### `base_handler.py`
**What it does**:
- Defines abstract base class for all format handlers
- Provides common functionality (normalization, metadata extraction)
- Ensures consistent interface across all handlers

**Key Class**: `BaseHandler`

### `registry.py`
**What it does**:
- Manages registration of all format handlers
- Selects appropriate handler for each file
- Provides list of supported formats

**Key Class**: `FormatRegistry`

### File Format Handlers

#### `excel_handler.py`
**What it does**:
- Reads Excel files (.xlsx, .xls, .xlsm)
- Extracts all sheets
- Converts to structured data
- Generates text representation

**Supports**: Multiple sheets, formulas, formatting

#### `csv_handler.py`
**What it does**:
- Reads CSV files
- Handles different delimiters
- Detects encoding
- Normalizes data

#### `json_handler.py`
**What it does**:
- Reads JSON files
- Handles nested structures
- Validates JSON syntax
- Flattens complex structures

#### `pdf_handler.py`
**What it does**:
- Extracts text from PDF files
- Extracts tables (using pdfplumber)
- Handles multi-page documents
- Preserves document structure

#### `word_handler.py`
**What it does**:
- Reads Word documents (.docx)
- Extracts paragraphs
- Extracts tables
- Preserves formatting

#### `ppt_handler.py`
**What it does**:
- Reads PowerPoint files (.pptx)
- Extracts slide content
- Extracts tables from slides
- Preserves slide structure

#### `image_handler.py`
**What it does**:
- Reads image files (PNG, JPG, etc.)
- Extracts EXIF metadata
- Performs OCR (optional)
- Provides image information

#### `text_handler.py`
**What it does**:
- Reads text files (.txt, .md, .log)
- Parses XML, YAML, TOML, INI
- Handles different encodings
- Preserves structure

#### `archive_handler.py`
**What it does**:
- Reads archive files (ZIP, TAR, GZ)
- Lists files in archive
- Can extract files (optional)
- Provides archive metadata

### Enterprise Connectors

#### `database_handler.py`
**What it does**:
- Connects to SQL databases (PostgreSQL, MySQL, SQL Server, etc.)
- Connects to MongoDB
- Executes queries
- Extracts tables/collections
- Converts to structured data

**Supports**: 6 database types

#### `enterprise_connectors.py`
**What it does**:
- Connects to CRM systems (Salesforce, HubSpot, Dynamics)
- Connects to ERP systems (SAP, Oracle ERP, NetSuite)
- Connects to cloud storage (OneDrive, Google Drive)
- Extracts data via APIs
- Handles authentication

**Supports**: 8 enterprise systems

### Metadata Extraction

#### `metadata_extractor.py`
**What it does**:
- Extracts rich metadata from files
- Gets file properties (author, dates, size)
- Extracts entities (names, locations, organizations)
- Extracts key terms
- Generates content signatures (hashes)

**Key Class**: `MetadataExtractor`

---

## 🧹 Cleaning Layer (`src/cleaning/`)

**Purpose**: Normalize, deduplicate, and validate data

### `normalizer.py`
**What it does**:
- Standardizes column names
- Normalizes data types
- Handles missing values
- Converts formats

### `deduplicator.py`
**What it does**:
- Removes exact duplicates
- Detects fuzzy duplicates
- Uses record linkage algorithms
- Preserves unique records

### `validator.py`
**What it does**:
- Validates data against schemas
- Checks data types
- Validates ranges
- Reports validation errors

### `pipeline.py`
**What it does**:
- Orchestrates cleaning steps
- Applies cleaning rules
- Tracks cleaning statistics
- Manages cleaning configuration

---

## 🔒 Redaction Layer (`src/redaction/`)

**Purpose**: Detect and redact PII/PHI

### `pii_detector.py`
**What it does**:
- Detects PII using Presidio (ML-based)
- Uses custom regex patterns
- Identifies: emails, phones, SSNs, credit cards
- Provides confidence scores

**Key Class**: `PIIDetector`

### `redactor.py`
**What it does**:
- Applies redaction strategies
- Masks, removes, or hashes PII
- Preserves data structure
- Tracks redaction statistics

**Key Class**: `DataRedactor`

### `pipeline.py`
**What it does**:
- Orchestrates detection and redaction
- Manages redaction configuration
- Tracks redaction statistics

---

## ✅ Compliance Layer (`src/compliance/`)

**Purpose**: Validate regulatory compliance

### `rules.py`
**What it does**:
- Defines compliance rules
- Implements GDPR, HIPAA, PCI-DSS, SOX rules
- Checks data requirements
- Validates consent flags

### `checker.py`
**What it does**:
- Validates data against regulations
- Generates compliance reports
- Identifies violations
- Provides remediation suggestions

**Key Class**: `ComplianceChecker`

---

## 📦 Batch Processing (`src/batch/`)

**Purpose**: Process multiple files in parallel

### `processor.py`
**What it does**:
- Scans directories for files
- Processes files in parallel
- Tracks progress
- Handles errors per file
- Supports resume capability

**Key Class**: `BatchProcessor`

### `file_scanner.py`
**What it does**:
- Scans directories recursively
- Filters files by pattern
- Collects file metadata
- Generates file lists

### `progress_tracker.py`
**What it does**:
- Tracks processing progress
- Shows progress bars
- Saves checkpoints
- Manages state

---

## 🔗 Relationship Detection (`src/relationships/`)

**Purpose**: Detect relationships between files

### `detector.py`
**What it does**:
- Orchestrates relationship detection
- Applies multiple strategies
- Calculates confidence scores
- Filters by threshold

**Key Class**: `RelationshipDetector`

### `strategies.py`
**What it does**:
- Implements detection strategies:
  - Content-based (shared entities, terms)
  - Filename matching
  - Metadata matching
- Calculates similarity scores
- Generates relationship evidence

**Key Classes**: `ContentStrategy`, `FilenameStrategy`, `MetadataStrategy`

### `graph.py`
**What it does**:
- Builds relationship graph
- Represents files as nodes
- Represents relationships as edges
- Exports graph to JSON

**Key Class**: `RelationshipGraph`

---

## 📊 Structuring Layer (`src/structuring/`)

**Purpose**: Format data for LLM training

### `agentic_formatter.py`
**What it does**:
- Formats data for agentic AI training
- Creates multi-file context
- Includes relationship information
- Generates synthetic reasoning
- Creates training prompts/completions

**Key Class**: `AgenticAIFormatter`

### `llm_formatter.py`
**What it does**:
- Formats single-file data for LLM training
- Combines structured data + text
- Includes human narration
- Creates training records

**Key Class**: `LLMFormatter`

### `formatter.py`
**What it does**:
- General data formatting
- Converts to JSONL, Parquet, CSV, JSON
- Handles different output formats

**Key Class**: `DataFormatter`

---

## 📤 Output Layer (`src/output/`)

**Purpose**: Write processed data to files

### `writer.py`
**What it does**:
- Writes data to various formats
- Creates output directories
- Handles file encoding
- Manages file paths

**Key Class**: `OutputWriter`

**Supported Formats**: JSONL, JSON, CSV, Parquet

---

## 🧪 Test Files

### `test_poc.py`
**Purpose**: Proof of concept test

**What it does**:
- Tests single file processing
- Demonstrates pipeline functionality
- Shows output format

---

## 📚 Documentation Files

### Root Documentation
- `README.md`: Overview and quick start
- `ARCHITECTURE.md`: System architecture
- `QUICK_START.md`: Getting started guide
- `BATCH_PROCESSING_GUIDE.md`: Batch processing guide
- `ENTERPRISE_CONNECTORS_GUIDE.md`: Enterprise system setup

### Docs Folder (`docs/`)
- `TECHNICAL.md`: Deep technical documentation
- `COMPONENTS.md`: This file (component guide)
- `API.md`: API reference
- `ENTERPRISE_CONNECTORS.md`: Enterprise connector details
- `RELATIONSHIPS.md`: Relationship detection details
- `AGENTIC_AI.md`: Agentic AI formatting details

---

## 🔄 Data Flow Summary

1. **Input** → `main.py` receives file/directory
2. **Ingestion** → Handler extracts data
3. **Cleaning** → Data normalized and validated
4. **Redaction** → PII detected and redacted
5. **Compliance** → Regulatory checks performed
6. **Relationships** → Files linked together
7. **Formatting** → Training data generated
8. **Output** → JSONL files written

---

## 🎯 Key Design Patterns

- **Strategy Pattern**: Different handlers for different formats
- **Factory Pattern**: Registry creates appropriate handlers
- **Pipeline Pattern**: Data flows through processing stages
- **Observer Pattern**: Progress tracking
- **Template Method**: Base handler defines structure

---

This component guide provides a high-level overview. For technical details, see [TECHNICAL.md](TECHNICAL.md).

