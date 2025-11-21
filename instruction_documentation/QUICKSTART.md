# Quick Start Guide

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install spaCy model for Presidio (PII detection):**
```bash
python -m spacy download en_core_web_sm
```

## Basic Usage

### Command Line

```bash
# Process a CSV file
python main.py --input data.csv --output processed_data.jsonl

# Process an Excel file with narration
python main.py --input data.xlsx --output training_data.jsonl --narration narration.txt

# Process with custom configuration
python main.py --input data.json --config config/example.yaml --output output.jsonl
```

### Python API

```python
from main import DataTransformationPipeline

# Initialize pipeline
pipeline = DataTransformationPipeline()

# Process data
results = pipeline.process(
    input_path='data.csv',
    output_path='output.jsonl',
    narration_path='narration.txt'
)

print(f"Processed {results['stats']['output_records']} records")
print(f"Output: {results['output_path']}")
```

## Supported Input Formats

- **Excel**: `.xlsx`, `.xls`, `.xlsm`
- **CSV**: `.csv`, `.tsv`
- **JSON**: `.json`
- **PowerPoint**: `.pptx`, `.ppt`
- **Databases**: PostgreSQL, MySQL, SQLite, MSSQL

## Output Format

The platform outputs data in JSONL format optimized for LLM training:

```json
{
  "id": "record_0",
  "structured_data": {...},
  "text_representation": "...",
  "human_narration": "...",
  "metadata": {...}
}
```

## Configuration

Create a `config.yaml` file to customize:

- Data cleaning settings
- PII redaction rules
- Compliance regulations to check
- Output format preferences

See `config/example.yaml` for a complete example.

## Next Steps

1. Review the compliance check results
2. Verify PII redaction was successful
3. Use the output JSONL file for LLM training
4. Integrate with your training pipeline

## Troubleshooting

**Issue**: Presidio analyzer errors
- **Solution**: Install spaCy model: `python -m spacy download en_core_web_sm`

**Issue**: Database connection fails
- **Solution**: Check connection string format: `postgresql://user:pass@host:port/db`

**Issue**: Memory errors with large files
- **Solution**: Use batch processing or increase system memory

