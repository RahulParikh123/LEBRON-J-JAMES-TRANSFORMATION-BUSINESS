# START HERE - Simple Step-by-Step Guide

## ✅ Everything is Already Done!

All the code is already written and saved. You don't need to write anything - just follow these steps.

## Step 1: Open Terminal/Command Prompt

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. OR use PowerShell (Windows Key + X, then select PowerShell)

## Step 2: Navigate to Your Project

Type this command (copy and paste):

```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
```

Press Enter.

## Step 3: Install Python Dependencies

Type this command:

```bash
pip install -r requirements.txt
```

This will take a few minutes. It's installing all the libraries the platform needs.

**If you get an error about pip:**
- You might need to install Python first: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

## Step 4: Install spaCy Language Model

Type this command:

```bash
python -m spacy download en_core_web_sm
```

This downloads a language model needed for detecting personal information.

## Step 5: Run the Test!

Type this command:

```bash
python test_poc.py
```

This will:
1. Create sample data files
2. Process them through the platform
3. Show you the results
4. Create output files ready for LLM training

## What You'll See

You should see output like:
```
Creating sample data files...
  - Creating sample CSV...
  - Creating sample JSON...
  ...

TEST 1: Processing CSV File
✓ Status: success
✓ Output: test_output/customers_processed.jsonl
...
```

## Step 6: Check the Results

After it finishes, you'll have:
- `test_data/` folder - Sample input files
- `test_output/` folder - Processed files ready for LLM training

Open the `test_output` folder to see your processed data!

## That's It! 🎉

You've successfully tested the platform!

## Next: Test with YOUR Data

1. Put your data file (CSV, Excel, JSON, etc.) in the project folder
2. Create a narration file (optional) - just a text file describing your data
3. Run:

```bash
python main.py --input YOUR_FILE.csv --output processed.jsonl --narration narration.txt
```

Replace `YOUR_FILE.csv` with your actual file name.

## Need Help?

If you get errors, check:
1. Did you install Python? (python --version)
2. Did you install dependencies? (pip install -r requirements.txt)
3. Are you in the right folder? (cd to the project folder)

