# Step-by-Step Testing Guide

## Quick Test with Your Files

I see you have a `LEBRON FILES` folder with test files! Let's use that.

### Step 1: Open Command Prompt or PowerShell

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
   - OR type `powershell` and press Enter

### Step 2: Navigate to Your Project Folder

Type this command and press Enter:

```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
```

### Step 3: Run the Test

You have two options:

#### Option A: Test with Your LEBRON FILES Folder
```bash
python test_batch.py --dir "LEBRON FILES"
```

#### Option B: Test with the Sample Test Data
```bash
python test_batch.py --dir "test_data"
```

### Step 4: Watch It Process

You'll see:
```
============================================================
Enterprise Data Transformation Platform - Batch Test
============================================================

Input directory: LEBRON FILES
Output directory: output
Relationship detection: Enabled

============================================================

Initializing pipeline...
Processing files...
Scanning directory: LEBRON FILES
Found 11 files (X.XX GB)
...
[Processing progress bar]
...
```

### Step 5: Check Results

After it finishes, check the `output` folder:

```
output/
├── summary.json                    ← Start here!
├── processed/                      ← Processed files
├── relationships/                  ← File relationships
├── metadata/                       ← File metadata
└── agentic_ai/                     ← Training data
```

## Detailed Steps

### Step 1: Verify Python is Working

In your command prompt, type:
```bash
python --version
```

You should see: `Python 3.14.0` (or similar)

### Step 2: Check You're in the Right Folder

Type:
```bash
dir test_batch.py
```

You should see the file listed. If not, navigate to the folder:
```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
```

### Step 3: Run the Test

**For your LEBRON FILES:**
```bash
python test_batch.py --dir "LEBRON FILES"
```

**For sample test data:**
```bash
python test_batch.py --dir "test_data"
```

### Step 4: What to Expect

1. **Scanning**: It will scan the folder for files
2. **Processing**: It will process each file (you'll see progress)
3. **Metadata**: It will extract metadata
4. **Relationships**: It will detect relationships between files
5. **Output**: It will create all output files

### Step 5: View Results

**Quick Summary:**
Open `output/summary.json` in any text editor

**Processed Files:**
Check `output/processed/` folder - each file becomes a `.jsonl` file

**Relationships:**
Check `output/relationships/relationship_graph.json` to see which files connect

**Agentic AI Data:**
Check `output/agentic_ai/training_data.jsonl` for training data

## Troubleshooting

### "python is not recognized"
- Python might not be in PATH
- Try: `python -m pip --version` to check
- Or use full path: `C:\Users\rahul\AppData\Local\Python\pythoncore-3.14-64\python.exe test_batch.py --dir "LEBRON FILES"`

### "No module named 'main'"
- Make sure you're in the project folder
- Type: `cd C:\Users\rahul\Downloads\data-transformation-platform`
- Then try again

### "Directory not found"
- Check the folder name (case-sensitive on some systems)
- Use quotes around folder names with spaces: `"LEBRON FILES"`

### Files Not Processing
- Check if files are supported formats (.xlsx, .pptx, .docx, .csv, .json)
- Check the console for error messages

## Example Full Command Sequence

```bash
# 1. Open command prompt (Windows Key + R, type "cmd")

# 2. Navigate to project
cd C:\Users\rahul\Downloads\data-transformation-platform

# 3. Verify files exist
dir test_batch.py
dir "LEBRON FILES"

# 4. Run the test
python test_batch.py --dir "LEBRON FILES"

# 5. Wait for it to finish (you'll see progress)

# 6. Check results
dir output
dir output\processed
dir output\relationships
```

## Quick Test Commands

**Test with LEBRON FILES:**
```bash
python test_batch.py --dir "LEBRON FILES"
```

**Test with sample data:**
```bash
python test_batch.py --dir "test_data"
```

**Test without relationship detection (faster):**
```bash
python test_batch.py --dir "LEBRON FILES" --no-relationships
```

**Custom output folder:**
```bash
python test_batch.py --dir "LEBRON FILES" --output "my_results"
```

## What Success Looks Like

At the end, you should see:
```
============================================================
BATCH PROCESSING COMPLETE!
============================================================

Files processed: 11
Relationships found: X

Output directory: output

Relationship graph: output\relationships\relationship_graph.json
Agentic AI training data: output\agentic_ai\training_data.jsonl

============================================================
Check the output directory for detailed results!
============================================================
```

## Next Steps After Testing

1. **Check summary.json** - Quick overview
2. **Review relationships** - See which files connect
3. **Check processed files** - See transformed data
4. **Review agentic AI data** - Training-ready format

---

**Ready to test? Just run:**
```bash
python test_batch.py --dir "LEBRON FILES"
```
