# API Reference

## Main Pipeline API

### `DataTransformationPipeline`

Main class for data transformation.

#### Initialization

```python
from main import DataTransformationPipeline

pipeline = DataTransformationPipeline(config=None)
```

**Parameters**:
- `config` (dict, optional): Configuration dictionary

#### Methods

##### `process(input_path, output_path=None, narration_path=None)`

Process a single file or data source.

**Parameters**:
- `input_path` (str): Path to input file or connection string
- `output_path` (str, optional): Path to output file (auto-generated if None)
- `narration_path` (str, optional): Path to human narration file

**Returns**:
```python
{
    'status': 'success' | 'failed',
    'output_path': str,
    'stats': {
        'cleaning': {...},
        'redaction': {...},
        'compliance': {...}
    }
}
```

**Example**:
```python
result = pipeline.process(
    input_path="data.xlsx",
    output_path="output/processed.jsonl"
)
```

##### `process_batch(input_directory, output_directory="output", detect_relationships=True, patterns=None, recursive=True)`

Process multiple files in batch with relationship detection.

**Parameters**:
- `input_directory` (str): Directory containing files to process
- `output_directory` (str): Output directory (default: "output")
- `detect_relationships` (bool): Whether to detect relationships (default: True)
- `patterns` (list, optional): File patterns to match (default: all supported)
- `recursive` (bool): Whether to scan subdirectories (default: True)

**Returns**:
```python
{
    'status': 'completed',
    'batch_results': {
        'files_processed': int,
        'files_failed': int,
        'completed_files': [str],
        'failed_files': [str]
    },
    'relationships_found': int,
    'output_directory': str,
    'relationship_graph': str,
    'agentic_ai_output': str
}
```

**Example**:
```python
result = pipeline.process_batch(
    input_directory="data_folder",
    output_directory="output",
    detect_relationships=True
)
```

---

## Format Registry API

### `FormatRegistry`

Manages format handlers.

#### Methods

##### `get_handler(file_path)`

Get appropriate handler for a file.

**Parameters**:
- `file_path` (str): Path to file

**Returns**: Handler instance or None

##### `get_supported_formats()`

Get list of all supported file extensions.

**Returns**: List of extensions (e.g., ['.xlsx', '.pdf', '.docx'])

##### `can_handle(file_path)`

Check if any handler can process the file.

**Parameters**:
- `file_path` (str): Path to file

**Returns**: bool

---

## Handler API

### `BaseHandler`

Base class for all format handlers.

#### Methods

##### `can_handle(file_path)`

Check if handler can process the file.

**Parameters**:
- `file_path` (str): Path to file

**Returns**: bool

##### `extract(source, **kwargs)`

Extract data from source.

**Parameters**:
- `source` (str): Source path or connection string
- `**kwargs`: Additional parameters

**Returns**:
```python
{
    'data': Any,  # Structured data
    'metadata': dict,
    'text_content': [str],
    'structure': dict
}
```

##### `get_supported_extensions()`

Get list of supported file extensions.

**Returns**: List of extensions

---

## Relationship Detection API

### `RelationshipDetector`

Detects relationships between files.

#### Methods

##### `detect_relationships(file_metadata_list, strategies=None, min_confidence=0.7)`

Detect relationships between files.

**Parameters**:
- `file_metadata_list` (list): List of file metadata dictionaries
- `strategies` (list, optional): Strategies to use (default: all)
- `min_confidence` (float): Minimum confidence threshold (default: 0.7)

**Returns**: List of relationship dictionaries

**Example**:
```python
from src.relationships.detector import RelationshipDetector

detector = RelationshipDetector()
relationships = detector.detect_relationships(
    file_metadata_list,
    min_confidence=0.7
)
```

---

## Agentic AI Formatter API

### `AgenticAIFormatter`

Formats data for agentic AI training.

#### Methods

##### `format_for_agentic_ai(file_data_list, relationship_graph=None, include_reasoning=True)`

Format files and relationships for agentic AI training.

**Parameters**:
- `file_data_list` (list): List of file data dictionaries
- `relationship_graph` (dict, optional): Relationship graph
- `include_reasoning` (bool): Include synthetic reasoning (default: True)

**Returns**:
```python
{
    'format': 'agentic_ai',
    'record_count': int,
    'content': [dict],  # Training records
    'metadata': {
        'total_files': int,
        'total_relationships': int
    }
}
```

---

## Batch Processor API

### `BatchProcessor`

Processes multiple files in batch.

#### Methods

##### `process_directory(input_directory, output_directory="output", patterns=None, recursive=True, process_func=None, **kwargs)`

Process directory of files.

**Parameters**:
- `input_directory` (str): Input directory
- `output_directory` (str): Output directory
- `patterns` (list, optional): File patterns
- `recursive` (bool): Scan subdirectories
- `process_func` (callable): Function to process each file
- `**kwargs`: Additional parameters

**Returns**: Batch processing results dictionary

---

## Connection Strings

### Database Connections

```
postgresql://user:password@host:port/database
mysql://user:password@host:port/database
mssql://user:password@host:port/database
sqlite:///path/to/database.db
oracle://user:password@host:port/service
mongodb://user:password@host:port/database
```

### Enterprise System Connections

```
salesforce://username:password@instance.salesforce.com
hubspot://api_key
dynamics://instance.crm.dynamics.com
sap://host:port
oracleerp://host:port
netsuite://account_id
onedrive://tenant_id
googledrive://project_id
```

---

For more details, see the [Technical Documentation](TECHNICAL.md).

