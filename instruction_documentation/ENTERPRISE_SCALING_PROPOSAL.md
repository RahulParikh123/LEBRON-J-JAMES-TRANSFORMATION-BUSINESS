# Enterprise Scaling & Multi-File Relationship Detection - Architecture Proposal

## Vision
Transform the platform from single-file processing to enterprise-scale batch processing with intelligent cross-file relationship detection for agentic AI training.

## Current State Analysis

### What We Have
- ✅ Single-file processing pipeline
- ✅ Format handlers (Excel, CSV, JSON, PPT, DB)
- ✅ Data cleaning, redaction, compliance
- ✅ LLM formatting (single file context)
- ✅ Basic metadata extraction

### What's Missing
- ❌ Batch processing of multiple files
- ❌ Cross-file relationship detection
- ❌ File metadata indexing
- ❌ Relationship graph construction
- ❌ Synthetic reasoning for linking files
- ❌ Agentic AI training format (multi-file context)
- ❌ Scalability for massive datasets

---

## Proposed Architecture

### Phase 1: Batch Processing Infrastructure

#### 1.1 New Component: `BatchProcessor`
**Location**: `src/batch/processor.py`

**Responsibilities**:
- Accept directory paths or file lists
- Queue files for processing
- Parallel processing (using Dask/ThreadPool)
- Progress tracking
- Error handling per file
- Resume capability

**Key Features**:
```python
class BatchProcessor:
    def process_directory(
        self, 
        input_dir: str,
        patterns: List[str] = ["*.xlsx", "*.csv", "*.pptx", "*.docx"],
        max_workers: int = 4,
        resume: bool = True
    ) -> BatchResults
```

#### 1.2 Enhanced Ingestion: Metadata Extraction
**Location**: `src/ingestion/metadata_extractor.py`

**Extract Rich Metadata**:
- File name patterns (e.g., "Q4_2024_Sales.xlsx")
- File timestamps (created, modified)
- File size and location
- Content signatures (hashes, key terms)
- Document properties (author, title, subject)
- Sheet names (for Excel)
- Slide titles (for PPT)
- Section headers (for Word)
- Embedded metadata (EXIF, custom properties)

**Metadata Schema**:
```python
{
    "file_id": "uuid",
    "file_path": "path/to/file.xlsx",
    "file_name": "Q4_2024_Sales.xlsx",
    "file_type": "excel",
    "file_size": 1024000,
    "created_at": "2024-10-01",
    "modified_at": "2024-11-15",
    "author": "John Doe",
    "title": "Q4 Sales Report",
    "content_signature": {
        "hash": "sha256...",
        "key_terms": ["sales", "revenue", "Q4"],
        "entities": ["Company A", "Product X"]
    },
    "structure": {
        "sheets": ["Sales", "Summary"],
        "columns": ["date", "amount", "product"],
        "row_count": 1000
    }
}
```

---

### Phase 2: Relationship Detection System

#### 2.1 New Component: `RelationshipDetector`
**Location**: `src/relationships/detector.py`

**Detection Strategies**:

1. **Filename Pattern Matching**
   - Extract patterns: "Q4_2024_Sales" → matches "Q4_2024_Sales_Presentation.pptx"
   - Fuzzy matching for variations
   - Date/version extraction

2. **Content-Based Linking**
   - Shared entities (company names, product IDs, project codes)
   - Shared data values (amounts, dates, IDs)
   - Semantic similarity (using embeddings)

3. **Metadata-Based Linking**
   - Same author/creator
   - Same project/topic
   - Temporal proximity (created around same time)
   - Location proximity (same directory/folder)

4. **Structure-Based Linking**
   - Excel sheet names match PPT slide titles
   - Column headers match Word section headers
   - Data schemas overlap

5. **Synthetic Reasoning**
   - Use LLM to infer relationships from context
   - Generate relationship descriptions
   - Confidence scoring

**Relationship Types**:
```python
RELATIONSHIP_TYPES = {
    "SUPPORTS": "Excel data supports PPT presentation",
    "SUMMARIZES": "PPT summarizes Excel data",
    "DOCUMENTS": "Word doc documents Excel analysis",
    "REFERENCES": "File A references data from File B",
    "VERSION_OF": "File A is newer version of File B",
    "RELATED_TO": "Files share common context/topic"
}
```

#### 2.2 Relationship Graph Builder
**Location**: `src/relationships/graph.py`

**Create Knowledge Graph**:
- Nodes: Files (with metadata)
- Edges: Relationships (with type, confidence, description)
- Store in graph database (NetworkX for small scale, Neo4j for enterprise)

**Graph Structure**:
```python
{
    "nodes": [
        {
            "id": "file_uuid_1",
            "type": "excel",
            "metadata": {...},
            "processed_data": "reference_to_data"
        }
    ],
    "edges": [
        {
            "source": "file_uuid_1",
            "target": "file_uuid_2",
            "relationship_type": "SUPPORTS",
            "confidence": 0.85,
            "evidence": ["shared_entities", "filename_pattern"],
            "description": "Sales data supports quarterly presentation"
        }
    ]
}
```

---

### Phase 3: Enhanced LLM Formatting for Agentic AI

#### 3.1 New Component: `AgenticAIFormatter`
**Location**: `src/structuring/agentic_formatter.py`

**Training Format for Agentic AI**:
- Multi-file context in single training record
- Relationship-aware formatting
- Action sequences (how files connect)
- Reasoning chains

**Output Format**:
```json
{
    "id": "training_record_001",
    "context": {
        "primary_file": {
            "file_id": "uuid_1",
            "file_name": "Q4_2024_Sales.xlsx",
            "structured_data": {...},
            "text_representation": "..."
        },
        "related_files": [
            {
                "file_id": "uuid_2",
                "file_name": "Q4_2024_Presentation.pptx",
                "relationship": "SUPPORTS",
                "relationship_description": "Presentation visualizes sales data",
                "structured_data": {...},
                "text_representation": "..."
            }
        ]
    },
    "relationships": [
        {
            "source": "uuid_1",
            "target": "uuid_2",
            "type": "SUPPORTS",
            "confidence": 0.85,
            "evidence": ["shared_entities", "temporal_proximity"],
            "reasoning": "The Excel file contains raw sales data that was used to create the PowerPoint presentation. Both files share the same project code and were created within 2 days of each other."
        }
    ],
    "synthetic_reasoning": {
        "abstraction": "This is a quarterly sales reporting workflow where raw data (Excel) is transformed into a presentation (PPT) for stakeholders.",
        "actions": [
            "Extract sales data from Excel",
            "Create visualizations",
            "Generate presentation slides",
            "Document findings in Word"
        ],
        "workflow": "Data Collection → Analysis → Visualization → Documentation"
    },
    "training_prompt": "Given an Excel file with sales data, identify related presentation and documentation files, and explain how they connect.",
    "training_completion": "The Excel file 'Q4_2024_Sales.xlsx' is connected to 'Q4_2024_Presentation.pptx' through a SUPPORTS relationship. The presentation visualizes the sales data, sharing entities like product names and revenue figures. Both files were created as part of the Q4 reporting workflow."
}
```

---

### Phase 4: Scalability Enhancements

#### 4.1 Distributed Processing
**Location**: `src/batch/distributed.py`

**Options**:
- **Dask**: For distributed DataFrame operations
- **Ray**: For distributed task execution (when Python 3.14 support available)
- **Celery**: For task queue management
- **Multiprocessing**: For local parallel processing

**Architecture**:
```
Master Node
    ↓
Task Queue (Redis/RabbitMQ)
    ↓
Worker Nodes (process files in parallel)
    ↓
Result Aggregator
    ↓
Relationship Detector
```

#### 4.2 Incremental Processing
- Process files in batches
- Store intermediate results
- Resume from checkpoints
- Update relationship graph incrementally

#### 4.3 Storage Strategy
- **Metadata Index**: SQLite/PostgreSQL for file metadata
- **Relationship Graph**: NetworkX (small) or Neo4j (large)
- **Processed Data**: Parquet files (columnar, efficient)
- **Training Data**: JSONL (streaming-friendly)

---

## Implementation Plan

### Step 1: Batch Processing (Week 1)
1. Create `src/batch/` module
2. Implement `BatchProcessor` class
3. Add directory scanning
4. Add parallel processing
5. Update `main.py` to support batch mode

### Step 2: Enhanced Metadata (Week 1-2)
1. Create `src/ingestion/metadata_extractor.py`
2. Enhance all handlers to extract rich metadata
3. Create metadata schema
4. Store metadata in index

### Step 3: Relationship Detection (Week 2-3)
1. Create `src/relationships/` module
2. Implement `RelationshipDetector` with multiple strategies
3. Create `RelationshipGraph` builder
4. Add confidence scoring
5. Test with sample file sets

### Step 4: Synthetic Reasoning (Week 3-4)
1. Integrate LLM API (OpenAI/Anthropic) for reasoning
2. Create abstraction generator
3. Create relationship description generator
4. Add reasoning chain builder

### Step 5: Agentic AI Formatter (Week 4)
1. Create `AgenticAIFormatter`
2. Implement multi-file context formatting
3. Add relationship-aware training records
4. Generate training prompts/completions

### Step 6: Scalability (Week 5)
1. Add distributed processing support
2. Implement incremental processing
3. Add checkpoint/resume capability
4. Optimize for large datasets

---

## New File Structure

```
src/
├── batch/
│   ├── __init__.py
│   ├── processor.py          # Batch file processor
│   ├── distributed.py         # Distributed processing
│   └── queue.py              # Task queue management
├── relationships/
│   ├── __init__.py
│   ├── detector.py           # Relationship detection
│   ├── graph.py              # Graph builder
│   ├── strategies.py         # Detection strategies
│   └── reasoning.py          # Synthetic reasoning
├── indexing/
│   ├── __init__.py
│   ├── metadata_index.py     # Metadata storage
│   └── content_index.py      # Content search index
├── ingestion/
│   ├── ... (existing)
│   └── metadata_extractor.py # Enhanced metadata extraction
└── structuring/
    ├── ... (existing)
    └── agentic_formatter.py  # Agentic AI formatting
```

---

## Configuration Changes

### New Config Section: `batch`
```yaml
batch:
  enabled: true
  input_directory: "/path/to/enterprise/data"
  patterns: ["*.xlsx", "*.csv", "*.pptx", "*.docx"]
  max_workers: 4
  chunk_size: 100  # Files per batch
  resume: true
```

### New Config Section: `relationships`
```yaml
relationships:
  enabled: true
  strategies:
    - filename_pattern
    - content_similarity
    - metadata_matching
    - semantic_similarity
    - synthetic_reasoning
  thresholds:
    min_confidence: 0.6
    semantic_similarity: 0.7
  llm_reasoning:
    enabled: true
    provider: "openai"  # or "anthropic"
    model: "gpt-4"
```

---

## Usage Examples

### Batch Processing
```python
from main import DataTransformationPipeline

pipeline = DataTransformationPipeline(config)

# Process entire directory
results = pipeline.process_batch(
    input_directory="/enterprise/data",
    output_directory="/processed/output",
    detect_relationships=True
)
```

### Relationship Detection
```python
from src.relationships.detector import RelationshipDetector

detector = RelationshipDetector()
relationships = detector.detect_relationships(
    file_metadata_list,
    strategies=["filename", "content", "semantic"]
)
```

### Agentic AI Training Data
```python
from src.structuring.agentic_formatter import AgenticAIFormatter

formatter = AgenticAIFormatter()
training_data = formatter.format_for_agentic_ai(
    file_data_list,
    relationship_graph,
    include_reasoning=True
)
```

---

## Benefits

1. **Scalability**: Process thousands of files in parallel
2. **Intelligence**: Automatically discover file relationships
3. **Context**: Multi-file context for better AI training
4. **Efficiency**: Incremental processing, resume capability
5. **Flexibility**: Multiple relationship detection strategies
6. **Agentic AI Ready**: Training format optimized for agentic AI

---

## Considerations

### Performance
- Relationship detection can be expensive (O(n²) comparisons)
- Use sampling for very large datasets
- Cache similarity scores
- Use approximate matching (LSH, MinHash)

### Accuracy
- Relationship detection may have false positives
- Confidence scores help filter
- Human review option for critical relationships

### Cost
- LLM-based reasoning has API costs
- Consider caching reasoning results
- Use cheaper models for bulk processing

### Privacy
- Relationship detection may reveal sensitive connections
- Ensure compliance with data policies
- Redact sensitive relationship information if needed

---

## Next Steps

1. **Review this proposal** - Does this align with your vision?
2. **Prioritize features** - Which phase should we start with?
3. **Define success metrics** - How will we measure relationship detection accuracy?
4. **Start implementation** - Begin with Phase 1 (Batch Processing)

---

**Questions to Consider:**
- What's your typical enterprise dataset size? (files, GB/TB)
- Do you have existing file organization patterns we can leverage?
- What types of relationships are most important? (temporal, content-based, structural?)
- Do you have access to LLM APIs for synthetic reasoning?
- What's your target accuracy for relationship detection?

