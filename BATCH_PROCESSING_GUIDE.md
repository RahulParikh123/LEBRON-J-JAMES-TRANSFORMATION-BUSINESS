# Batch Processing Guide - All 4 Phases Complete! 🎉

## Quick Start

### 1. Put Your Files in a Folder
```
my_test_data/
├── financials.docx
├── projections.xlsx
├── board_deck.pptx
└── ...
```

### 2. Run the Test Script
```bash
python test_batch.py --dir "my_test_data"
```

### 3. Check Results
Results will be in the `output/` folder:
- `processed/` - All processed files (JSONL format)
- `relationships/` - Relationship graph and summary
- `metadata/` - File metadata index
- `agentic_ai/` - Training data for agentic AI
- `summary.json` - Quick overview

## What You Get

### ✅ Phase 1: Batch Processing
- Processes all files in parallel
- Shows real-time progress
- Can resume if interrupted
- Handles errors gracefully

### ✅ Phase 2: Enhanced Metadata
- Extracts rich metadata from all files
- Author, title, structure, entities, key terms
- Stored in `output/metadata/file_metadata.json`

### ✅ Phase 3: Relationship Detection
- Content-based relationship detection
- Finds connections between files (e.g., Excel → PPT)
- Confidence scoring (default: 0.7+)
- Relationship graph in `output/relationships/`

### ✅ Phase 4: Agentic AI Formatting
- Multi-file context training data
- Relationship-aware formatting
- Synthetic reasoning chains
- Training prompts and completions

## Example Output Structure

```
output/
├── summary.json                    # Quick stats
├── processed/
│   ├── financials_processed.jsonl
│   ├── projections_processed.jsonl
│   └── board_deck_processed.jsonl
├── relationships/
│   ├── relationship_graph.json     # Full graph
│   └── relationships_summary.json  # Summary stats
├── metadata/
│   └── file_metadata.json         # All file metadata
└── agentic_ai/
    └── training_data.jsonl         # Agentic AI training data
```

## Command Options

```bash
# Basic usage
python test_batch.py --dir "my_data"

# Custom output directory
python test_batch.py --dir "my_data" --output "my_output"

# Skip relationship detection (faster)
python test_batch.py --dir "my_data" --no-relationships

# Use custom config
python test_batch.py --dir "my_data" --config "config.yaml"
```

## Relationship Types Detected

- **INFORMS**: File A provides data used in File B (e.g., Excel → PPT)
- **SUMMARIZES**: File A summarizes File B (e.g., PPT → Excel)
- **DOCUMENTS**: File A documents File B (e.g., Word → Excel)
- **RELATED_TO**: Files share common context

## Example Relationship

```json
{
  "source_file_name": "financials.docx",
  "target_file_name": "projections.xlsx",
  "relationship_type": "INFORMS",
  "confidence": 0.85,
  "evidence": [
    {
      "strategy": "ContentStrategy",
      "evidence": {
        "shared_entities": ["Revenue", "Q4-2024"],
        "shared_terms": ["financial", "projection", "revenue"]
      }
    }
  ]
}
```

## Agentic AI Training Data Format

Each training record includes:
- **Context**: Primary file + related files
- **Relationships**: How files connect
- **Synthetic Reasoning**: Workflow abstraction
- **Training Prompt**: "Given file X, identify related files..."
- **Training Completion**: Explanation of relationships

## Tips

1. **Start Small**: Test with 5-10 files first
2. **Check Summary**: Always check `output/summary.json` first
3. **Review Relationships**: Check `output/relationships/` to see connections
4. **Agentic AI Data**: Use `output/agentic_ai/training_data.jsonl` for training

## Troubleshooting

**No relationships found?**
- Check if files share common entities/terms
- Lower confidence threshold in config
- Ensure metadata extraction worked

**Processing slow?**
- Reduce `max_workers` in config
- Skip relationship detection with `--no-relationships`

**Errors?**
- Check logs in console
- Review `output/checkpoints/batch_state.json` for failed files

## Next Steps

1. Test with your data files
2. Review relationship graph
3. Use agentic AI training data for model training
4. Customize config for your needs

---

**All 4 phases are complete and ready to test!** 🚀

