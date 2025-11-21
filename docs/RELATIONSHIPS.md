# Relationship Detection

## Overview

The platform automatically detects relationships between files using multiple strategies, enabling multi-file context for agentic AI training.

---

## Detection Strategies

### 1. Content-Based Strategy

**What it does**: Analyzes file content to find shared entities and key terms.

**How it works**:
1. Extracts entities (names, locations, organizations, dates)
2. Extracts key terms (important words/phrases)
3. Calculates Jaccard similarity on shared entities/terms
4. Scores relationship confidence

**Example**:
- File A mentions "Starbucks Corporation" and "Q4 2024"
- File B mentions "Starbucks Corporation" and "Q4 2024"
- **Relationship detected**: High confidence (shared entities + terms)

**Confidence Calculation**:
```python
shared_entities = set(entities1) & set(entities2)
shared_terms = set(terms1) & set(terms2)

entity_similarity = len(shared_entities) / len(set(entities1) | set(entities2))
term_similarity = len(shared_terms) / len(set(terms1) | set(terms2))

confidence = (entity_similarity * 0.6) + (term_similarity * 0.4)
```

### 2. Filename Strategy

**What it does**: Matches files based on naming patterns.

**How it works**:
1. Extracts base filename (without extension)
2. Calculates Levenshtein distance
3. Checks for version numbers, dates, project codes
4. Scores similarity

**Example**:
- `FNP_ATZ_PJ_V2.pptx`
- `FNP_ATZ_PJ_V2 (1).pptx`
- **Relationship detected**: 95% filename similarity

**Pattern Matching**:
- Version numbers: `_v1`, `_v2`, `(1)`, `(2)`
- Dates: `Q4_2024`, `2024-01-15`
- Project codes: `FNP_ATZ`, `SBUX`

### 3. Metadata Strategy

**What it does**: Matches files based on metadata (author, dates, project names).

**How it works**:
1. Compares author names
2. Checks temporal proximity (created/modified dates)
3. Matches titles/subjects
4. Checks directory location

**Example**:
- File A: Author "Karen Phua", Modified "2023-09-14"
- File B: Author "Karen Phua", Modified "2023-09-15"
- **Relationship detected**: Same author, 1 day apart

**Matching Criteria**:
- Same author: +0.3 confidence
- Same directory: +0.2 confidence
- Within 7 days: +0.2 confidence
- Title similarity: +0.3 confidence

---

## Relationship Types

### INFORMS
File A provides data/information used in File B.

**Example**: Excel spreadsheet → PowerPoint presentation

### INFORMED_BY
File A is informed by File B (reverse of INFORMS).

**Example**: PowerPoint presentation ← Excel spreadsheet

### SUMMARIZES
File A summarizes content from File B.

**Example**: Executive summary → Full report

### RELATED_TO
Files share common context or topic.

**Example**: Two presentations about the same company

---

## Confidence Scoring

### Threshold
Default minimum confidence: **0.7** (70%)

### Scoring Factors

1. **Content Similarity** (40% weight)
   - Shared entities
   - Shared key terms
   - Semantic similarity

2. **Filename Similarity** (30% weight)
   - Levenshtein distance
   - Pattern matching
   - Base name matching

3. **Metadata Matching** (30% weight)
   - Author matching
   - Temporal proximity
   - Title similarity
   - Directory location

### Combined Score
```python
confidence = (
    content_score * 0.4 +
    filename_score * 0.3 +
    metadata_score * 0.3
)
```

---

## Relationship Graph

### Structure

```json
{
  "nodes": [
    {
      "id": "file_id_1",
      "file_name": "financials.xlsx",
      "file_type": "excel",
      "metadata": {...}
    }
  ],
  "edges": [
    {
      "source": "file_id_1",
      "target": "file_id_2",
      "type": "INFORMS",
      "confidence": 0.95,
      "evidence": [...],
      "reasoning": "..."
    }
  ]
}
```

### Graph Properties

- **Nodes**: Files (with metadata)
- **Edges**: Relationships (with confidence, evidence)
- **Directed**: Relationships have direction
- **Weighted**: Confidence scores as weights

---

## Usage

### Automatic Detection

Relationship detection runs automatically during batch processing:

```python
result = pipeline.process_batch(
    input_directory="data_folder",
    detect_relationships=True  # Default: True
)
```

### Manual Detection

```python
from src.relationships.detector import RelationshipDetector

detector = RelationshipDetector()
relationships = detector.detect_relationships(
    file_metadata_list,
    strategies=['content', 'filename', 'metadata'],
    min_confidence=0.7
)
```

### Accessing Relationships

```python
# From batch results
result = pipeline.process_batch(...)
relationship_graph_path = result['relationship_graph']

# Load graph
import json
with open(relationship_graph_path) as f:
    graph = json.load(f)

# Access relationships
for edge in graph['edges']:
    print(f"{edge['source']} -> {edge['target']}: {edge['type']} ({edge['confidence']})")
```

---

## Configuration

### Minimum Confidence

```yaml
relationships:
  min_confidence: 0.7  # Adjust threshold
```

### Strategy Selection

```yaml
relationships:
  strategies:
    - content      # Content-based matching
    - filename     # Filename matching
    - metadata     # Metadata matching
```

### Weights

```python
# Customize strategy weights
detector = RelationshipDetector()
detector.strategy_weights = {
    'content': 0.5,
    'filename': 0.3,
    'metadata': 0.2
}
```

---

## Performance

### Complexity
- **Time**: O(n²) comparisons for n files
- **Optimization**: Early termination for low-confidence matches
- **Parallelization**: Can process in parallel

### Scalability
- **100 files**: ~5 seconds
- **1000 files**: ~5 minutes
- **Optimization**: Sampling for very large datasets

---

## Examples

### Example 1: Excel → PowerPoint

**Files**:
- `Q4_Sales.xlsx` (Excel with sales data)
- `Q4_Presentation.pptx` (PowerPoint with sales charts)

**Detection**:
- Content: Shared entities ("Q4", "Sales", "Revenue")
- Filename: Both start with "Q4_"
- Metadata: Same author, created same day

**Result**: `INFORMS` relationship, 0.92 confidence

### Example 2: Word → Excel

**Files**:
- `Financial_Report.docx` (Word document)
- `Financial_Model.xlsx` (Excel model)

**Detection**:
- Content: Shared financial terms
- Filename: Both start with "Financial_"
- Metadata: Same project code

**Result**: `RELATED_TO` relationship, 0.78 confidence

---

## Limitations

1. **False Positives**: May detect relationships that don't exist
2. **False Negatives**: May miss relationships
3. **Language Dependent**: Works best with English content
4. **Content Quality**: Requires meaningful content in files

---

## Future Enhancements

- [ ] Semantic embeddings for better matching
- [ ] Machine learning-based detection
- [ ] Cross-language relationship detection
- [ ] Temporal relationship patterns

---

For implementation details, see [Technical Documentation](TECHNICAL.md).

