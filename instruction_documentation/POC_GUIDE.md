# POC Test Guide - Data Transformation Platform

## ✅ Confirmed: Platform is Ready!

I can see your data transformation platform with all the components:
- ✅ Main pipeline (`main.py`)
- ✅ Test POC script (`test_poc.py`)
- ✅ All source modules (ingestion, cleaning, redaction, compliance, structuring, output)
- ✅ Configuration files
- ✅ Python 3.14.0 installed

## Step-by-Step POC Test

### Step 1: Install Dependencies

Open PowerShell or Command Prompt in this folder and run:

```powershell
python -m pip install pandas numpy pyarrow openpyxl python-pptx sqlalchemy pydantic pyyaml fuzzywuzzy python-Levenshtein recordlinkage presidio-analyzer presidio-anonymizer spacy psycopg2-binary pymysql boto3 dask tqdm python-dotenv loguru pytest pytest-cov
```

**Note:** We're skipping `ray` because it doesn't support Python 3.14 yet. It's optional for distributed computing and not needed for the POC.

### Step 2: Install spaCy Language Model

```powershell
python -m spacy download en_core_web_sm
```

This is needed for PII (Personal Identifiable Information) detection.

### Step 3: Run the POC Test

```powershell
python test_poc.py
```

This will:
1. Create sample test data (CSV, JSON, Excel files)
2. Process them through the transformation pipeline
3. Show you the results
4. Create output files in `test_output/` folder

### Step 4: Review Results

After the test completes, check:
- `test_data/` folder - Sample input files created
- `test_output/` folder - Processed files ready for LLM training

## What the POC Tests

1. **CSV Processing** - Processes customer data with PII
2. **JSON Processing** - Processes product catalog
3. **Excel Processing** - Processes multi-sheet sales data
4. **Custom Configuration** - Tests with custom settings

## Expected Output

You should see:
```
============================================================
Enterprise Data Transformation Platform - POC Test
============================================================

Creating sample data files...
  - Creating sample CSV...
  - Creating sample JSON...
  - Creating sample Excel...
  - Creating sample narration...

============================================================
TEST 1: Processing CSV File
============================================================
✓ Status: success
✓ Output: test_output/customers_processed.jsonl
...
```

## Troubleshooting

**If dependencies fail to install:**
- Make sure you're in the project folder
- Try: `python -m pip install --upgrade pip` first
- Then install packages one by one if needed

**If spaCy model fails:**
- Try: `python -m pip install spacy` first
- Then: `python -m spacy download en_core_web_sm`

## Next Steps After POC

Once the POC works, you can:
1. Process your own data files
2. Use `main.py` with your data
3. Customize configuration in `config/example.yaml`

