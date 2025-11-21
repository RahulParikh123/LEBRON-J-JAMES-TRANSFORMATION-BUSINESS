# Sample Files

This directory contains sample input and output files from a real test run of the transformation pipeline.

## Input Files

### `East West Bancorp Model V2.xlsx`
- **Type**: Excel financial model
- **Content**: Financial data with multiple sheets
- **Size**: ~1.1 MB
- **Sheets**: 4 sheets (Misc Data + Calculations, Net Income Build, IEA Yield + IBL Cost Build, DCF)

### `Sherry_Hu_Resume.docx`
- **Type**: Word document
- **Content**: Resume/CV document
- **Size**: ~34 KB
- **Structure**: Contains tables and text

### `FNP_ATZ_PJ_V2.pptx`
- **Type**: PowerPoint presentation
- **Content**: Business presentation slides
- **Size**: ~1.1 MB
- **Slides**: 8 slides with text and content

## Processed Output Files

### `East West Bancorp Model V2_processed.jsonl`
- **Format**: JSONL (JSON Lines)
- **Content**: Transformed Excel data with:
  - Structured data from all sheets
  - Text representation
  - Metadata (author, dates, structure)
  - Processing stats (cleaning, redaction, compliance)

### `Sherry_Hu_Resume_processed.jsonl`
- **Format**: JSONL
- **Content**: Transformed Word document with:
  - Paragraphs and tables
  - Text representation
  - Metadata
  - Processing stats

### `FNP_ATZ_PJ_V2_processed.jsonl`
- **Format**: JSONL
- **Content**: Transformed PowerPoint with:
  - Slide content
  - Text representation
  - Metadata
  - Processing stats

## How to Use

These files demonstrate:
1. **Input**: Original file formats
2. **Output**: Transformed, LLM-ready JSONL format

You can:
- Compare input vs output to understand transformations
- Use as reference for expected output format
- Test the pipeline with these files

## Processing These Files

```bash
# Process the sample files
python test_batch.py --dir "samples"
```

This will process the input files and generate new outputs (which should match the existing processed files).

---

**Note**: These files are from a real test run and demonstrate the complete transformation pipeline from raw enterprise files to LLM-training-ready data.

