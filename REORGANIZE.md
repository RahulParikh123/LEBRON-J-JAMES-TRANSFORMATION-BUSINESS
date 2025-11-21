# Repository Reorganization Plan

## New Structure

```
LEBRON-J-JAMES-TRANSFORMATION-BUSINESS/
├── code/                          # All source code
│   ├── src/                       # Source code
│   ├── main.py                    # Main pipeline
│   ├── test_batch.py              # Test scripts
│   ├── view_redaction_info.py     # Tools
│   ├── requirements.txt           # Dependencies
│   └── setup.py                   # Setup file
│
├── instruction_documentation/     # All documentation
│   ├── README.md                  # Main overview
│   ├── QUICK_START.md            # Getting started
│   ├── ARCHITECTURE.md           # Architecture
│   ├── PROJECT_SUMMARY.md        # Summary
│   └── docs/                     # Detailed docs
│       ├── TECHNICAL.md
│       ├── COMPONENTS.md
│       ├── API.md
│       └── ...
│
├── processed_outputs/            # Processed JSONL files
│   ├── East West Bancorp Model V2_processed.jsonl
│   ├── Sherry_Hu_Resume_processed.jsonl
│   ├── FNP_ATZ_PJ_V2_processed.jsonl
│   └── ... (all other processed files)
│
├── samples/                      # Sample input files
│   ├── East West Bancorp Model V2.xlsx
│   ├── Sherry_Hu_Resume.docx
│   └── FNP_ATZ_PJ_V2.pptx
│
└── .gitignore                    # Git ignore rules
```

