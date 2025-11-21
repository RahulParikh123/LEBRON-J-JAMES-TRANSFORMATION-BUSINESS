# Agentic AI Formatting

## Overview

The platform generates LLM training data optimized for agentic AI, with multi-file context and relationship awareness.

---

## What is Agentic AI Training Data?

Agentic AI needs to understand:
1. **Multi-file context**: How files relate to each other
2. **Workflows**: How data flows between files
3. **Actions**: What actions can be taken with files
4. **Reasoning**: Why files are connected

This platform generates training data that teaches AI these concepts.

---

## Training Data Format

### Structure

```json
{
  "id": "training_record_<file_id>",
  "context": {
    "primary_file": {
      "file_id": "...",
      "file_name": "financials.xlsx",
      "file_type": "excel",
      "structured_data": {
        "Sheet1": {
          "data": [...],
          "columns": [...]
        }
      },
      "text_representation": "Sheet: Sheet1\nColumns: revenue, expenses...",
      "metadata": {...}
    },
    "related_files": [
      {
        "file_id": "...",
        "file_name": "presentation.pptx",
        "file_type": "powerpoint",
        "relationship": "INFORMS",
        "confidence": 0.95,
        "structured_data": {...},
        "text_representation": "...",
        "metadata": {...}
      }
    ]
  },
  "relationships": [
    {
      "source": "file_id_1",
      "target": "file_id_2",
      "type": "INFORMS",
      "confidence": 0.95,
      "evidence": [...],
      "reasoning": "..."
    }
  ],
  "synthetic_reasoning": {
    "abstraction": "This is a data processing workflow...",
    "workflow": "Data Collection → Analysis → Visualization",
    "actions": [
      "Extract data from financials.xlsx",
      "Create visualizations",
      "Generate presentation.pptx"
    ]
  },
  "training_prompt": "Given financials.xlsx, identify related files...",
  "training_completion": "The file is connected to presentation.pptx..."
}
```

---

## Key Components

### 1. Primary File Context

The main file being processed:
- Full structured data
- Text representation
- Complete metadata
- Processing stats

### 2. Related Files Context

Files related to the primary file:
- Relationship type (INFORMS, RELATED_TO, etc.)
- Confidence score
- Structured data
- Text representation
- Metadata

### 3. Relationships

Explicit relationship information:
- Source and target files
- Relationship type
- Confidence score
- Evidence (why the relationship exists)
- Reasoning (human-readable explanation)

### 4. Synthetic Reasoning

AI-generated reasoning about the workflow:
- **Abstraction**: High-level description
- **Workflow**: Data flow pattern
- **Actions**: Sequence of actions

**Example**:
```json
{
  "abstraction": "This is a quarterly reporting workflow where raw data (Excel) is transformed into a presentation (PPT) for stakeholders.",
  "workflow": "Data Collection → Analysis → Visualization → Documentation",
  "actions": [
    "Extract sales data from Excel",
    "Create visualizations",
    "Generate presentation slides",
    "Document findings in Word"
  ]
}
```

### 5. Training Prompt/Completion

Ready-to-use training examples:
- **Prompt**: Question about the file/relationship
- **Completion**: Expected answer

**Example**:
```
Prompt: "Given financials.xlsx, identify related files and explain how they connect."

Completion: "The file 'financials.xlsx' is connected to:
- 'presentation.pptx' through a INFORMS relationship: The Excel file provides data used in the presentation
- 'report.docx' through a SUMMARIZES relationship: The Word document summarizes the Excel data

Workflow: Data Collection → Analysis → Visualization → Documentation
Abstraction: This is a quarterly reporting workflow..."
```

---

## Workflow Inference

The system infers workflows from file types:

### Common Workflows

1. **Documentation → Data Analysis → Presentation**
   - Word → Excel → PowerPoint

2. **Data Collection → Visualization**
   - Excel → PowerPoint

3. **Documentation → Data Processing**
   - Word → Excel

4. **Data Processing Workflow**
   - Generic multi-file workflow

### Inference Logic

```python
def infer_workflow(primary_file, related_files):
    file_types = [primary_file.type] + [rf.type for rf in related_files]
    
    if 'word' in file_types and 'excel' in file_types and 'powerpoint' in file_types:
        return "Documentation → Data Analysis → Presentation"
    elif 'excel' in file_types and 'powerpoint' in file_types:
        return "Data Collection → Visualization"
    # ... more patterns
```

---

## Abstraction Generation

High-level description of the file relationship:

**Template**:
```
"This is a {workflow} where {primary_file} {relationship} {related_files}."
```

**Example**:
```
"This is a data processing workflow where financials.xlsx connects to 2 related files: presentation.pptx, report.docx."
```

---

## Action Sequence Generation

List of actions the AI can take:

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

## Usage

### Automatic Generation

Generated automatically during batch processing:

```python
result = pipeline.process_batch(
    input_directory="data_folder",
    detect_relationships=True  # Required for agentic AI formatting
)

# Training data is in:
training_data_path = result['agentic_ai_output']
```

### Manual Generation

```python
from src.structuring.agentic_formatter import AgenticAIFormatter

formatter = AgenticAIFormatter()
training_data = formatter.format_for_agentic_ai(
    file_data_list,
    relationship_graph,
    include_reasoning=True
)
```

### Accessing Training Data

```python
import json

with open('output/agentic_ai/training_data.jsonl') as f:
    for line in f:
        record = json.loads(line)
        print(record['training_prompt'])
        print(record['training_completion'])
        print()
```

---

## Configuration

### Include Reasoning

```python
formatter = AgenticAIFormatter(config={
    'include_reasoning': True  # Generate synthetic reasoning
})
```

### Relationship Threshold

Only include relationships above confidence threshold:

```python
# In relationship detection
relationships = detector.detect_relationships(
    file_metadata_list,
    min_confidence=0.7  # Only high-confidence relationships
)
```

---

## Use Cases

### 1. Multi-File Understanding

Train AI to understand how files relate:
- Excel spreadsheet informs PowerPoint presentation
- Word document summarizes Excel data
- Multiple files form a workflow

### 2. Workflow Learning

Train AI to recognize workflows:
- Data collection → Analysis → Visualization
- Documentation → Data Processing → Presentation

### 3. Action Generation

Train AI to generate actions:
- "Extract data from Excel"
- "Create visualizations"
- "Generate presentation"

### 4. Context Awareness

Train AI to use multi-file context:
- When asked about Excel, AI knows related PowerPoint exists
- AI can reference related files in responses
- AI understands file relationships

---

## Output Format

### JSONL (JSON Lines)

Each line is a complete training record:

```
{"id": "record_1", "context": {...}, ...}
{"id": "record_2", "context": {...}, ...}
{"id": "record_3", "context": {...}, ...}
```

**Benefits**:
- Streaming-friendly
- Easy to process line-by-line
- Standard format for LLM training

---

## Performance

- **Generation Speed**: ~100 records/second
- **Memory Usage**: Minimal (streaming output)
- **Scalability**: Handles 1000+ files

---

## Limitations

### Current Implementation

- **Rule-based reasoning**: No LLM API (can be added)
- **Template-based**: Uses patterns, not ML
- **Language**: English-focused

### Future Enhancements

- [ ] LLM-based reasoning (OpenAI, Anthropic)
- [ ] Local LLM support (Ollama, LM Studio)
- [ ] Multi-language support
- [ ] Custom reasoning templates

---

## Example Training Record

See `samples/*_processed.jsonl` for complete examples of transformed files.

See `output/agentic_ai/training_data.jsonl` for complete training records with relationships.

---

For implementation details, see [Technical Documentation](TECHNICAL.md).

