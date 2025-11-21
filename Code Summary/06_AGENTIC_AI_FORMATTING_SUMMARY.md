# Agentic AI Formatting - Code Summary

## Overview
The Agentic AI Formatting layer generates LLM training data optimized for agentic AI, with multi-file context, relationship awareness, and synthetic reasoning chains.

---

## Key Components

### 1. Agentic AI Formatter (`agentic_formatter.py`)
**Purpose**: Formats data for agentic AI training with multi-file context

**Key Methods**:
- `format_for_agentic_ai(file_data_list, relationship_graph)`: Creates training records
- Returns formatted training data with relationships and reasoning

---

### 2. Training Record Structure

**Each training record contains**:

**1. Primary File Context**:
- Full structured data
- Text representation
- Complete metadata
- Processing stats

**2. Related Files Context**:
- Files related to primary file
- Relationship type (INFORMS, RELATED_TO, etc.)
- Confidence score
- Structured data from related files
- Text representation

**3. Relationships**:
- Explicit relationship information
- Source and target files
- Relationship type
- Evidence (why the relationship exists)
- Reasoning (human-readable explanation)

**4. Synthetic Reasoning**:
- **Abstraction**: High-level description of workflow
- **Workflow**: Data flow pattern (e.g., "Data Collection → Analysis → Visualization")
- **Actions**: Sequence of actions AI can take

**5. Training Prompt/Completion**:
- **Prompt**: Question about the file/relationship
- **Completion**: Expected answer for LLM training

---

### 3. Workflow Inference

**Purpose**: Infers workflows from file types

**Common Workflows**:
- **Documentation → Data Analysis → Presentation**: Word → Excel → PowerPoint
- **Data Collection → Visualization**: Excel → PowerPoint
- **Documentation → Data Processing**: Word → Excel
- **Data Processing Workflow**: Generic multi-file workflow

**How it works**:
- Analyzes file types in relationship
- Matches against known workflow patterns
- Generates workflow description

---

### 4. Abstraction Generation

**Purpose**: Creates high-level description of file relationships

**Template**:
```
"This is a {workflow} where {primary_file} {relationship} {related_files}."
```

**Example**:
```
"This is a data processing workflow where financials.xlsx connects to 2 related files: presentation.pptx, report.docx."
```

---

### 5. Action Sequence Generation

**Purpose**: Generates list of actions AI can take

**Example**:
```json
{
  "actions": [
    "Extract data from financials.xlsx",
    "Create visualizations",
    "Generate presentation.pptx",
    "Document findings in report.docx"
  ]
}
```

**Generation Logic**:
- Based on relationship types
- Based on file types
- Based on workflow patterns

---

## Data Flow

```
Processed Files + Relationship Graph
    ↓
For Each File:
    ├── Get Related Files
    ├── Build Context
    ├── Generate Reasoning
    └── Create Training Record
    ↓
Training Records
    ├── Multi-file context
    ├── Relationships
    ├── Synthetic reasoning
    └── Training prompts/completions
    ↓
JSONL Output
```

---

## Training Record Format

```json
{
  "id": "training_record_<file_id>",
  "context": {
    "primary_file": {
      "file_id": "...",
      "file_name": "financials.xlsx",
      "structured_data": {...},
      "text_representation": "...",
      "metadata": {...}
    },
    "related_files": [
      {
        "file_name": "presentation.pptx",
        "relationship": "INFORMS",
        "confidence": 0.95,
        "structured_data": {...},
        "text_representation": "..."
      }
    ]
  },
  "relationships": [...],
  "synthetic_reasoning": {
    "abstraction": "This is a quarterly reporting workflow...",
    "workflow": "Data Collection → Analysis → Visualization",
    "actions": ["Extract data...", "Create visualizations..."]
  },
  "training_prompt": "Given financials.xlsx, identify related files...",
  "training_completion": "The file is connected to presentation.pptx..."
}
```

---

## Synthetic Reasoning Generation

**Currently Rule-Based** (no LLM API):
- Uses pattern matching on file types
- Template-based abstraction generation
- Hardcoded action patterns

**Future Enhancement**: Can add LLM-based reasoning (OpenAI, Anthropic, local LLM)

---

## Key Methods

**`format_for_agentic_ai()`**:
- Main method to format all files
- Creates training records for each file
- Includes relationships and reasoning

**`_create_training_record()`**:
- Creates single training record
- Builds context (primary + related files)
- Generates reasoning and prompts

**`_generate_synthetic_reasoning()`**:
- Generates abstraction, workflow, actions
- Rule-based (no LLM required)

**`_generate_training_prompt_completion()`**:
- Creates prompt/completion pairs
- Ready for LLM training

---

## Output Format

**JSONL (JSON Lines)**:
- Each line is a complete training record
- Streaming-friendly
- Standard format for LLM training

**Benefits**:
- Easy to process line-by-line
- Can handle large datasets
- Standard format

---

## Key Design Patterns

- **Builder Pattern**: Builds complex training records
- **Template Method**: Base reasoning generation structure
- **Strategy Pattern**: Different reasoning strategies (future)

---

## Output

Returns:
- **Training records**: List of complete training records
- **Format**: 'agentic_ai'
- **Record count**: Number of training records
- **Metadata**: Total files, relationships, etc.

---

## Use Cases

**1. Multi-File Understanding**:
- Train AI to understand how files relate
- Excel spreadsheet informs PowerPoint presentation
- Word document summarizes Excel data

**2. Workflow Learning**:
- Train AI to recognize workflows
- Data collection → Analysis → Visualization

**3. Action Generation**:
- Train AI to generate actions
- "Extract data from Excel"
- "Create visualizations"

**4. Context Awareness**:
- Train AI to use multi-file context
- When asked about Excel, AI knows related PowerPoint exists
- AI can reference related files in responses

