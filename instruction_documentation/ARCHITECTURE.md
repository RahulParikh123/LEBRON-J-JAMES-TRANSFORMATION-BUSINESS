# System Architecture

## Overview

The LEBRON-J'JAMES-TRANSFORMATION-BUSINESS platform is built on a modular, pipeline-based architecture designed for enterprise-scale data processing.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│              Data Transformation Pipeline                     │
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
                  │   Output     │
                  │  (JSONL)     │
                  └──────────────┘
```

---

## Layer Breakdown

### 1. Ingestion Layer

**Purpose**: Extract data from diverse sources

**Components**:
- Format handlers (40+ file types)
- Enterprise connectors (databases, CRM, ERP, cloud)
- Metadata extractors

**Key Features**:
- Auto-detection of file types
- Unified interface for all sources
- Parallel processing support

### 2. Cleaning Layer

**Purpose**: Normalize and validate data

**Components**:
- Data normalizer
- Deduplicator
- Validator

**Key Features**:
- Type standardization
- Duplicate removal (exact + fuzzy)
- Schema validation

### 3. Redaction Layer

**Purpose**: Detect and redact PII/PHI

**Components**:
- PII detector (Presidio + custom)
- Data redactor
- Redaction pipeline

**Key Features**:
- ML-based detection
- Multiple redaction strategies
- Compliance-ready output

### 4. Compliance Layer

**Purpose**: Validate regulatory compliance

**Components**:
- Compliance rules (GDPR, HIPAA, PCI-DSS, SOX)
- Compliance checker

**Key Features**:
- Multi-regulation support
- Automated validation
- Compliance reporting

### 5. Relationship Detection

**Purpose**: Link related files

**Components**:
- Content-based matching
- Filename pattern matching
- Metadata matching

**Key Features**:
- Multi-strategy detection
- Confidence scoring
- Relationship graph construction

### 6. Agentic AI Formatting

**Purpose**: Generate LLM training data

**Components**:
- Multi-file context builder
- Relationship formatter
- Synthetic reasoning generator

**Key Features**:
- Multi-file context
- Relationship awareness
- Training prompt/completion generation

---

## Data Flow

### Single File Flow

```
File → Handler → Extract → Clean → Redact → Check → Format → Output
```

### Batch Flow

```
Directory → Scan → Parallel Process → Collect Metadata → 
Detect Relationships → Build Graph → Format → Training Data
```

---

## Design Principles

1. **Modularity**: Each layer is independent and replaceable
2. **Extensibility**: Easy to add new handlers/connectors
3. **Scalability**: Designed for enterprise-scale processing
4. **Reliability**: Error handling at every layer
5. **Performance**: Parallel processing where possible

---

## Technology Stack

- **Language**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **Database**: SQLAlchemy
- **PII Detection**: Presidio
- **Parallel Processing**: Concurrent.futures
- **Progress Tracking**: tqdm

---

## Scalability Features

- **Parallel Processing**: Multi-threaded file processing
- **Batch Processing**: Handles 100+ files simultaneously
- **Resume Capability**: Can resume interrupted jobs
- **Memory Efficient**: Streaming for large files
- **Error Isolation**: One file failure doesn't stop batch

---

## Extension Points

1. **New File Handlers**: Add to `src/ingestion/`
2. **New Enterprise Connectors**: Add to `src/ingestion/enterprise_connectors.py`
3. **New Relationship Strategies**: Add to `src/relationships/strategies.py`
4. **Custom Processing**: Extend pipeline in `main.py`

---

For detailed technical documentation, see [docs/TECHNICAL.md](docs/TECHNICAL.md).
