# 🚀 QUICK TEST - Copy & Paste These Commands

## Easiest Way (Using Files That Already Exist)

**Just copy and paste these 3 commands one by one:**

### 1. Navigate to the project folder
```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
```

### 2. Run the test
```bash
python test_batch.py --dir "test_data"
```

### 3. Check results
```bash
dir output
```

**That's it!** The test will use the sample files that are already in your `test_data` folder.

---

## What You'll See

```
============================================================
Enterprise Data Transformation Platform - Batch Test
============================================================

Input directory: test_data
Output directory: output
Relationship detection: Enabled

============================================================

Initializing pipeline...
Processing files...
Scanning directory: test_data
Found 3 files (0.00 GB)
Processing files...
[████████████████████] 100% (3/3 files)

BATCH PROCESSING COMPLETE!
============================================================

Files processed: 3
Relationships found: 2
...
```

---

## Where Are the Results?

After running, check this folder:
```
C:\Users\rahul\Downloads\data-transformation-platform\output\
```

Open it in File Explorer to see:
- `processed/` - Processed files
- `relationships/` - File connections
- `summary.json` - Quick summary

---

## Test With Your Own Files

1. **Create a folder** (e.g., `C:\Users\rahul\Downloads\my_files`)
2. **Put your files in it** (Excel, CSV, PPT, Word, JSON)
3. **Run**:
   ```bash
   python test_batch.py --dir "C:\Users\rahul\Downloads\my_files"
   ```

---

## Still Having Issues?

1. **Make sure you're in the right folder:**
   ```bash
   cd C:\Users\rahul\Downloads\data-transformation-platform
   ```

2. **Check Python works:**
   ```bash
   python --version
   ```
   (Should show: Python 3.14.0)

3. **Check the file exists:**
   ```bash
   dir test_batch.py
   ```
   (Should show: test_batch.py)

4. **If Python doesn't work, try:**
   ```bash
   py test_batch.py --dir "test_data"
   ```

---

**That's all you need! Just 2 commands to test!** ✅

