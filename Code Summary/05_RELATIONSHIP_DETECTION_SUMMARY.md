# Relationship Detection - Code Summary

## Overview
The Relationship Detection system intelligently identifies connections between files using multiple strategies (content-based, filename, metadata) to build a relationship graph for multi-file context.

---

## Key Components

### 1. Relationship Detector (`detector.py`)
**Purpose**: Orchestrates relationship detection between all files

**Key Methods**:
- `detect_relationships(file_metadata_list)`: Detects relationships between all file pairs
- Returns list of relationships with confidence scores

**Relationship Types**:
- `INFORMS`: File A provides data used in File B
- `SUMMARIZES`: File A summarizes File B
- `DOCUMENTS`: File A documents File B
- `REFERENCES`: File A references File B
- `RELATED_TO`: Files share common context

---

### 2. Detection Strategies (`strategies.py`)

**1. Content Strategy** (`ContentStrategy`):
**Purpose**: Finds relationships based on shared content

**How it works**:
- Extracts entities (names, locations, organizations) from each file
- Extracts key terms (important words/phrases)
- Calculates Jaccard similarity on shared entities/terms
- Scores relationship confidence

**Example**:
- File A: "Starbucks Corporation", "Q4 2024"
- File B: "Starbucks Corporation", "Q4 2024"
- **Result**: High confidence relationship (shared entities + terms)

**Confidence Calculation**:
```python
shared_entities = set(entities1) & set(entities2)
shared_terms = set(terms1) & set(terms2)

entity_similarity = len(shared_entities) / len(set(entities1) | set(entities2))
term_similarity = len(shared_terms) / len(set(terms1) | set(terms2))

confidence = (entity_similarity * 0.6) + (term_similarity * 0.4)
```

---

**2. Filename Strategy** (`FilenameStrategy`):
**Purpose**: Matches files based on naming patterns

**How it works**:
- Extracts base filename (without extension)
- Calculates Levenshtein distance
- Checks for version numbers, dates, project codes
- Scores similarity

**Pattern Matching**:
- Version numbers: `_v1`, `_v2`, `(1)`, `(2)`
- Dates: `Q4_2024`, `2024-01-15`
- Project codes: `FNP_ATZ`, `SBUX`

**Example**:
- `FNP_ATZ_PJ_V2.pptx` vs `FNP_ATZ_PJ_V2 (1).pptx`
- **Result**: 95% filename similarity

---

**3. Metadata Strategy** (`MetadataStrategy`):
**Purpose**: Matches files based on metadata

**How it works**:
- Compares author names
- Checks temporal proximity (created/modified dates)
- Matches titles/subjects
- Checks directory location

**Matching Criteria**:
- Same author: +0.3 confidence
- Same directory: +0.2 confidence
- Within 7 days: +0.2 confidence
- Title similarity: +0.3 confidence

**Example**:
- File A: Author "Karen Phua", Modified "2023-09-14"
- File B: Author "Karen Phua", Modified "2023-09-15"
- **Result**: Same author, 1 day apart → relationship detected

---

**4. Semantic Strategy** (`SemanticStrategy`) - Optional:
**Purpose**: Uses semantic embeddings for deeper matching

**How it works**:
- Generates embeddings using sentence-transformers
- Calculates cosine similarity
- Finds semantically similar content

**Note**: Requires `sentence-transformers` library (optional)

---

### 3. Relationship Graph (`graph.py`)
**Purpose**: Builds and manages the relationship graph

**Graph Structure**:
- **Nodes**: Files (with metadata)
- **Edges**: Relationships (with confidence, evidence)
- **Directed**: Relationships have direction
- **Weighted**: Confidence scores as weights

**Key Methods**:
- `add_node(file_metadata)`: Add file to graph
- `add_edge(relationship)`: Add relationship
- `to_dict()`: Export graph to JSON
- `get_related_files(file_id)`: Get all files related to a file

---

## Detection Process

```
File Metadata List
    ↓
For Each File Pair:
    ├── Content Strategy
    ├── Filename Strategy
    └── Metadata Strategy
    ↓
Combine Evidence
    ↓
Calculate Confidence
    ↓
Filter by Threshold (default: 0.7)
    ↓
Relationship List
    ↓
Build Relationship Graph
```

---

## Confidence Scoring

**Combined Score**:
```python
confidence = (
    content_score * 0.4 +
    filename_score * 0.3 +
    metadata_score * 0.3
)
```

**Threshold**: Default minimum confidence: 0.7 (70%)

**Scoring Factors**:
1. **Content Similarity** (40% weight)
   - Shared entities
   - Shared key terms
   - Semantic similarity

2. **Filename Similarity** (30% weight)
   - Levenshtein distance
   - Pattern matching

3. **Metadata Matching** (30% weight)
   - Author matching
   - Temporal proximity
   - Title similarity

---

## Output Format

**Relationship**:
```python
{
    'source_file_id': 'uuid_1',
    'source_file_name': 'financials.xlsx',
    'target_file_id': 'uuid_2',
    'target_file_name': 'presentation.pptx',
    'relationship_type': 'INFORMS',
    'relationship_description': 'File A provides data used in File B',
    'confidence': 0.95,
    'evidence': [
        {
            'strategy': 'ContentStrategy',
            'evidence': {
                'shared_entities': ['Starbucks', 'Q4'],
                'shared_terms': ['revenue', 'sales']
            }
        }
    ],
    'evidence_count': 1
}
```

**Graph**:
```python
{
    'nodes': [file_metadata_list],
    'edges': [relationship_list]
}
```

---

## Performance

**Complexity**: O(n²) - compares every file with every other file
- **100 files**: ~500 comparisons (fast)
- **1,000 files**: ~500,000 comparisons (~30 minutes)
- **10,000 files**: ~50 million comparisons (~8 hours)

**Optimization**:
- Early termination for low-confidence matches
- Can process in parallel
- Sampling for very large datasets

---

## Key Design Patterns

- **Strategy Pattern**: Multiple detection strategies
- **Graph Pattern**: Relationship graph structure
- **Evidence-Based**: Combines evidence from multiple sources

---

## Output

Returns:
- **Relationships**: List of all detected relationships
- **Graph**: Complete relationship graph structure
- **Statistics**: Summary of relationships by type
- **Evidence**: Detailed evidence for each relationship

