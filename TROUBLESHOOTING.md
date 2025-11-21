# Troubleshooting Guide

## Problem: BAT File Runs But No Output

### Step 1: Check What Happened

The BAT file window might have closed too fast. Let's check:

1. **Open Command Prompt** (Windows Key + R, type `cmd`)
2. **Navigate to your folder:**
   ```bash
   cd C:\Users\rahul\Downloads\data-transformation-platform
   ```
3. **Run the command manually:**
   ```bash
   python main.py --input "HOME Model v4.xlsx" --output processed.jsonl
   ```

This will show you any error messages!

### Step 2: Common Issues and Fixes

#### Issue 1: "Python is not recognized"

**Problem:** Python isn't installed or not in PATH

**Fix:**
1. Install Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your computer
4. Try again

#### Issue 2: "No module named 'pandas'" or similar

**Problem:** Dependencies aren't installed

**Fix:**
```bash
pip install -r requirements.txt
```

This will take a few minutes. Wait for it to finish.

#### Issue 3: "File not found" or "No handler found"

**Problem:** File path issue or format not supported

**Fix:**
- Make sure the file is in the project folder
- Check the exact file name (case-sensitive!)
- Make sure it's a supported format (CSV, Excel, JSON, PPT)

#### Issue 4: File is locked/being used

**Problem:** Excel file is open in Excel

**Fix:**
- Close Excel
- Close any programs using the file
- Try again

#### Issue 5: "Permission denied"

**Problem:** Don't have permission to write output

**Fix:**
- Run Command Prompt as Administrator
- Or change output location:
  ```bash
  python main.py --input "HOME Model v4.xlsx" --output "C:\Users\rahul\Desktop\processed.jsonl"
  ```

### Step 3: Check Output Location

The output might be in different places:

1. **`output/` folder** - Most common location
2. **Current directory** - Same folder as your script
3. **Where you specified** - If you used `--output` with a path

**To find it:**
```bash
# In Command Prompt, in your project folder:
dir /s *.jsonl
```

This will search for all JSONL files.

### Step 4: Run Step-by-Step

Let's test each part:

**Test 1: Check Python works**
```bash
python --version
```
Should show Python version (like "Python 3.11.0")

**Test 2: Check dependencies**
```bash
python -c "import pandas; print('OK')"
```
Should print "OK"

**Test 3: Check file exists**
```bash
dir "HOME Model v4.xlsx"
```
Should show the file

**Test 4: Try processing**
```bash
python main.py --input "HOME Model v4.xlsx" --output test.jsonl
```

### Step 5: Get Detailed Error Messages

If it still doesn't work, run with verbose output:

```bash
python main.py --input "HOME Model v4.xlsx" --output test.jsonl --log-level DEBUG
```

This will show more details about what's happening.

## Alternative: Use Python Directly

If BAT files aren't working, use Python directly:

1. **Open Command Prompt**
2. **Go to your project folder:**
   ```bash
   cd C:\Users\rahul\Downloads\data-transformation-platform
   ```
3. **Run:**
   ```bash
   python main.py --input "HOME Model v4.xlsx" --output processed.jsonl
   ```

This way you'll see all error messages.

## Still Having Issues?

1. **Copy the exact error message** you see
2. **Check:**
   - Python version: `python --version`
   - File exists: `dir "HOME Model v4.xlsx"`
   - Dependencies: `pip list | findstr pandas`
3. **Try the test script first:**
   ```bash
   python test_poc.py
   ```
   This will tell you if the platform works at all.

## Quick Diagnostic Script

Run this to check everything:

```bash
@echo off
echo Checking setup...
python --version
echo.
echo Checking file...
dir "HOME Model v4.xlsx"
echo.
echo Checking dependencies...
python -c "import pandas; print('Dependencies OK')"
echo.
echo Ready to process!
pause
```

Save this as `check_setup.bat` and run it to see what's missing.

