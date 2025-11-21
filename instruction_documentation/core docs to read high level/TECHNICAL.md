# Technical Documentation

## Deep Technical Details

This document provides comprehensive technical documentation for the LEBRON-J'JAMES-TRANSFORMATION-BUSINESS platform.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Core Components](#core-components)
3. [Data Flow](#data-flow)
4. [Implementation Details](#implementation-details)
5. [Performance Considerations](#performance-considerations)
6. [Extension Points](#extension-points)

---

## System Architecture

### High-Level Architecture

The platform follows a modular, pipeline-based architecture:

```
Input Sources
    │
    ├── Files (40+ formats)
    ├── Databases (6 types)
    ├── CRM Systems (3)
    ├── ERP Systems (3)
    └── Cloud Storage (2)
    │
    ▼
┌─────────────────────────────────────┐
│      Ingestion Layer                │
│  - Format Handlers                  │
│  - Enterprise Connectors            │
│  - Metadata Extraction              │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌──────────┐      ┌──────────────┐
│ Cleaning │      │  Redaction   │
│ Pipeline │─────▶│   Pipeline   │
└────┬─────┘      └──────┬───────┘
     │                    │
     └──────────┬─────────┘
                │
                ▼
         ┌──────────────┐
         │  Compliance  │
         │   Checking   │
         └──────┬───────┘
                │
                ▼
      ┌──────────────────┐
      │   Relationship   │
      │    Detection     │
      └────────┬─────────┘
               │
               ▼
      ┌──────────────────┐
      │  Agentic AI      │
      │   Formatting      │
      └────────┬──────────┘
               │
               ▼
         Output (JSONL)
```

### Component Layers

#### 1. Ingestion Layer (`src/ingestion/`)

**Purpose**: Extract data from diverse sources

**Key Classes**:
- `BaseHandler`: Abstract base for all handlers
- `FormatRegistry`: Handler registration and selection
- Format-specific handlers (Excel, PDF, Word, etc.)
- Enterprise connectors (Salesforce, SAP, etc.)

**Design Pattern**: Strategy Pattern + Factory Pattern

**Key Methods**:
```python
class BaseHandler(ABC):
    @abstractmethod
    def can_handle(self, file_path: str) -> bool
    
    @abstractmethod
    def extract(self, source: str, **kwargs) -> Dict[str, Any]
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]
```

**Handler Registration**:
```python
registry = FormatRegistry()
# Handlers auto-registered on initialization
handler = registry.get_handler(file_path)
```

#### 2. Cleaning Layer (`src/cleaning/`)

**Purpose**: Normalize, deduplicate, validate data

**Components**:
- `DataNormalizer`: Standardizes data structure
- `DataDeduplicator`: Removes duplicates (exact + fuzzy)
- `DataValidator`: Schema validation
- `CleaningPipeline`: Orchestrates cleaning steps

**Algorithms**:
- Fuzzy matching: Levenshtein distance
- Deduplication: Record linkage algorithms
- Type inference: Pandas-based type detection

#### 3. Redaction Layer (`src/redaction/`)

**Purpose**: Detect and redact PII/PHI

**Components**:
- `PIIDetector`: Uses Presidio + custom patterns
- `DataRedactor`: Applies redaction strategies
- `RedactionPipeline`: Orchestrates detection/redaction

**Detection Methods**:
1. Presidio Analyzer (ML-based)
2. Regex patterns (custom)
3. Pattern matching (SSN, credit cards, etc.)

**Redaction Strategies**:
- `mask`: Replace with asterisks
- `remove`: Delete entirely
- `hash`: Replace with hash
- `replace`: Replace with placeholder

#### 4. Compliance Layer (`src/compliance/`)

**Purpose**: Validate regulatory compliance

**Supported Regulations**:
- GDPR (General Data Protection Regulation)
- HIPAA (Health Insurance Portability)
- PCI-DSS (Payment Card Industry)
- SOX (Sarbanes-Oxley)

**Implementation**:
- Rule-based validation
- Pattern matching for sensitive data
- Compliance scoring

#### 5. Relationship Detection (`src/relationships/`)

**Purpose**: Detect relationships between files

**Strategies**:
1. **ContentStrategy**: Shared entities, key terms, semantic similarity
2. **FilenameStrategy**: Filename pattern matching
3. **MetadataStrategy**: Author, dates, project names

**Algorithm**:
```python
def detect_relationships(metadata_list):
    relationships = []
    for i, file1 in enumerate(metadata_list):
        for file2 in metadata_list[i+1:]:
            confidence = calculate_confidence(file1, file2)
            if confidence >= threshold:
                relationships.append(create_relationship(file1, file2))
    return relationships
```

**Confidence Calculation**:
- Content similarity: Jaccard similarity on entities/terms
- Filename similarity: Levenshtein distance
- Metadata matching: Exact + fuzzy matching
- Combined: Weighted average

#### 6. Agentic AI Formatting (`src/structuring/`)

**Purpose**: Generate LLM training data with multi-file context

**Output Format**:
```json
{
  "id": "training_record_...",
  "context": {
    "primary_file": {
      "file_id": "...",
      "structured_data": {...},
      "text_representation": "...",
      "metadata": {...}
    },
    "related_files": [...]
  },
  "relationships": [...],
  "synthetic_reasoning": {...},
  "training_prompt": "...",
  "training_completion": "..."
}
```

**Synthetic Reasoning**:
- Workflow inference from file types
- Abstraction generation
- Action sequence generation
- Currently rule-based (no LLM API)

---

## Core Components

### Main Pipeline (`main.py`)

**Class**: `DataTransformationPipeline`

**Responsibilities**:
- Orchestrate entire transformation pipeline
- Manage component lifecycle
- Handle batch processing
- Coordinate relationship detection

**Key Methods**:
```python
def process(input_path, output_path, narration_path=None)
    # Single file processing

def process_batch(input_directory, output_directory, ...)
    # Batch processing with relationship detection
```

### Batch Processor (`src/batch/processor.py`)

**Class**: `BatchProcessor`

**Features**:
- Parallel file processing
- Progress tracking
- Checkpoint/resume capability
- Error handling per file

**Implementation**:
- Uses `concurrent.futures.ThreadPoolExecutor`
- Progress bar with `tqdm`
- State persistence in JSON

### Metadata Extractor (`src/ingestion/metadata_extractor.py`)

**Class**: `MetadataExtractor`

**Extracts**:
- File metadata (size, dates, author)
- Content signatures (hash, entities, key terms)
- Structure information (sheets, slides, sections)
- Document properties

**Entity Extraction**:
- Pattern-based (no LLM required)
- Extracts: names, locations, organizations, dates
- Key term extraction: TF-IDF based

---

## Data Flow

### Single File Processing Flow

```
1. Input File
   │
   ▼
2. Format Detection (FormatRegistry)
   │
   ▼
3. Handler Selection
   │
   ▼
4. Data Extraction
   │
   ├── Structured Data
   ├── Text Representation
   └── Metadata
   │
   ▼
5. Cleaning Pipeline
   │
   ├── Normalization
   ├── Deduplication
   └── Validation
   │
   ▼
6. Redaction Pipeline
   │
   ├── PII Detection
   └── Redaction
   │
   ▼
7. Compliance Checking
   │
   ▼
8. LLM Formatting
   │
   ▼
9. Output (JSONL)
```

### Batch Processing Flow

```
1. Directory Scan
   │
   ▼
2. File Discovery
   │
   ▼
3. Parallel Processing (per file)
   │
   ├── Extract
   ├── Clean
   ├── Redact
   └── Format
   │
   ▼
4. Metadata Collection
   │
   ▼
5. Relationship Detection
   │
   ├── Content Analysis
   ├── Filename Matching
   └── Metadata Matching
   │
   ▼
6. Relationship Graph Construction
   │
   ▼
7. Agentic AI Formatting
   │
   ├── Multi-file Context
   ├── Relationship Links
   └── Synthetic Reasoning
   │
   ▼
8. Training Data Output
```

---

## Implementation Details

### Handler Pattern

All handlers inherit from `BaseHandler`:

```python
class BaseHandler(ABC):
    def normalize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        # Standardizes column names and types
        # Converts all values to strings
        
    def extract_metadata(self, source: str) -> Dict[str, Any]:
        # Extracts basic file metadata
```

**Handler Implementation Example**:
```python
class ExcelHandler(BaseHandler):
    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith(('.xlsx', '.xls', '.xlsm'))
    
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        # Read Excel file
        # Extract all sheets
        # Normalize data
        # Generate text representation
        return {
            'data': sheets_data,
            'metadata': metadata,
            'text_content': text_content,
            'structure': structure
        }
```

### Relationship Detection Algorithm

**Content-Based Matching**:
```python
def calculate_content_similarity(file1, file2):
    # Extract entities and key terms
    entities1 = extract_entities(file1)
    entities2 = extract_entities(file2)
    
    # Calculate Jaccard similarity
    shared_entities = set(entities1) & set(entities2)
    similarity = len(shared_entities) / len(set(entities1) | set(entities2))
    
    return similarity
```

**Filename Matching**:
```python
def calculate_filename_similarity(name1, name2):
    # Levenshtein distance
    distance = levenshtein(name1, name2)
    max_len = max(len(name1), len(name2))
    similarity = 1 - (distance / max_len)
    
    return similarity
```

### Batch Processing Parallelism

```python
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {
        executor.submit(process_file, file): file 
        for file in files_to_process
    }
    
    for future in as_completed(futures):
        file = futures[future]
        try:
            result = future.result()
            # Handle success
        except Exception as e:
            # Handle error
```

---

## Performance Considerations

### Memory Management

- **Streaming**: Large files processed in chunks
- **Lazy Loading**: Handlers load data on-demand
- **Garbage Collection**: Explicit cleanup after processing

### Parallel Processing

- **Thread Pool**: Uses ThreadPoolExecutor for I/O-bound tasks
- **Worker Count**: Configurable (default: 4)
- **Progress Tracking**: Real-time progress updates

### Scalability

- **Batch Size**: Configurable chunk size
- **Checkpointing**: Can resume interrupted jobs
- **Error Isolation**: One file failure doesn't stop batch

### Optimization Strategies

1. **Caching**: Metadata cached to avoid re-extraction
2. **Lazy Evaluation**: Relationships computed on-demand
3. **Batch Operations**: Group similar operations

---

## Extension Points

### Adding New File Handlers

1. Create handler class:
```python
class NewFormatHandler(BaseHandler):
    def can_handle(self, file_path: str) -> bool:
        return file_path.endswith('.newformat')
    
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        # Implementation
        pass
    
    def get_supported_extensions(self) -> List[str]:
        return ['.newformat']
```

2. Register in `src/ingestion/registry.py`:
```python
from .new_format_handler import NewFormatHandler

default_handlers = [
    # ... existing handlers
    NewFormatHandler(),
]
```

### Adding Enterprise Connectors

1. Create connector class:
```python
class NewSystemConnector(BaseHandler):
    def can_handle(self, source: str) -> bool:
        return source.startswith('newsystem://')
    
    def extract(self, source: str, **kwargs) -> Dict[str, Any]:
        # API connection logic
        pass
```

2. Register in registry

### Custom Relationship Strategies

1. Create strategy class:
```python
class CustomStrategy(RelationshipStrategy):
    def detect(self, file1, file2) -> Optional[Relationship]:
        # Custom detection logic
        pass
```

2. Register in `src/relationships/detector.py`

---

## Technical Stack

- **Python**: 3.8+
- **Pandas**: Data manipulation
- **SQLAlchemy**: Database connections
- **Presidio**: PII detection
- **spaCy**: NLP (optional)
- **Concurrent.futures**: Parallel processing
- **tqdm**: Progress bars

---

## Error Handling

### Strategy

- **Per-File Errors**: Isolated, don't stop batch
- **Graceful Degradation**: Fallback to simpler methods
- **Error Logging**: Comprehensive error tracking
- **Resume Capability**: Can retry failed files

### Error Types

1. **File Format Errors**: Unsupported or corrupted files
2. **Connection Errors**: Database/API failures
3. **Processing Errors**: Data transformation failures
4. **Memory Errors**: Large file handling

---

## Testing

### Unit Tests

- Handler tests
- Pipeline component tests
- Relationship detection tests

### Integration Tests

- End-to-end pipeline tests
- Batch processing tests
- Enterprise connector tests

### Performance Tests

- Large file processing
- Batch throughput
- Memory usage

---

## Security Considerations

- **Credential Management**: Environment variables, no hardcoding
- **Data Isolation**: Per-file processing isolation
- **PII Handling**: Secure redaction, no logging of sensitive data
- **Connection Security**: Encrypted database connections

---

This technical documentation provides the deep dive into system internals. For component-level documentation, see [COMPONENTS.md](COMPONENTS.md).

