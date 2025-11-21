# How to Run with YOUR Actual Data

## Quick Answer

**To test with sample data:** Run `test_poc.py` (creates sample data automatically)
**To process YOUR actual data:** Use `main.py` with your file

## Option 1: Test with Sample Data First (Recommended)

This creates sample data and tests everything:

### Using PowerShell Script (Easiest):
1. **Right-click** `run_test.ps1`
2. Select **"Run with PowerShell"**
3. Wait for it to finish
4. Check the `test_output` folder for results

### Using Command Line:
```bash
python test_poc.py
```

**What this does:**
- Creates sample CSV, JSON, Excel files
- Processes them
- Shows you how it works
- Outputs to `test_output/` folder

## Option 2: Process YOUR Actual Data

### Step 1: Prepare Your Data File

1. Put your data file in the project folder:
   - CSV file (`.csv`)
   - Excel file (`.xlsx`, `.xls`)
   - JSON file (`.json`)
   - PowerPoint (`.pptx`)

2. (Optional) Create a narration file:
   - Create a text file (`.txt`)
   - Write a description of your data
   - Example: "This dataset contains customer sales data from Q1 2024..."

### Step 2: Open Command Prompt

1. Press `Windows Key + R`
2. Type `cmd` and press Enter

### Step 3: Navigate to Project Folder

```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
```

### Step 4: Run with Your File

**Basic command:**
```bash
python main.py --input YOUR_FILE.csv --output processed.jsonl
```

**With narration:**
```bash
python main.py --input YOUR_FILE.csv --output processed.jsonl --narration narration.txt
```

**With custom config:**
```bash
python main.py --input YOUR_FILE.xlsx --output processed.jsonl --config config/example.yaml
```

### Step 5: Check Results

1. Look in the `output/` folder (or wherever you specified)
2. Open the `.jsonl` file - it's ready for LLM training!

## Examples

### Example 1: Process a CSV file
```bash
python main.py --input customers.csv --output customers_processed.jsonl
```

### Example 2: Process Excel with narration
```bash
python main.py --input sales_data.xlsx --output sales_processed.jsonl --narration sales_description.txt
```

### Example 3: Process JSON file
```bash
python main.py --input products.json --output products_processed.jsonl
```

## What Happens When You Run It

1. **Ingestion** - Reads your file
2. **Cleaning** - Normalizes and removes duplicates
3. **Redaction** - Removes/masks personal information
4. **Compliance** - Checks GDPR/HIPAA compliance
5. **Formatting** - Formats for LLM training
6. **Output** - Creates JSONL file

You'll see progress messages like:
```
Starting data transformation for: customers.csv
Step 1: Ingesting data...
Step 2: Cleaning data...
Step 3: Detecting and redacting PII/PHI...
...
Processing completed successfully!
```

## Troubleshooting

**Error: "No handler found"**
- Your file format might not be supported
- Supported: CSV, Excel, JSON, PowerPoint, Databases

**Error: "File not found"**
- Make sure your file is in the project folder
- Or use full path: `--input "C:\path\to\your\file.csv"`

**Error: "Python not found"**
- Install Python first
- Make sure it's added to PATH

## Quick Reference

| What You Want | Command |
|--------------|---------|
| Test with sample data | `python test_poc.py` |
| Process your CSV | `python main.py --input file.csv --output result.jsonl` |
| Process Excel | `python main.py --input file.xlsx --output result.jsonl` |
| With narration | Add `--narration narration.txt` |
| With config | Add `--config config/example.yaml` |

## Summary

1. **Test first:** Run `python test_poc.py` to see how it works
2. **Then use your data:** Run `python main.py --input YOUR_FILE --output result.jsonl`
3. **Check output:** Look in `output/` folder for processed file

That's it! 🎉

