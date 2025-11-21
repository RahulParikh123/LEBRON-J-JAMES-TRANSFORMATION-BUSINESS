# How to Edit the Code

## Opening Files to Edit

### Option 1: Using File Explorer
1. Open File Explorer
2. Navigate to: `C:\Users\rahul\Downloads\data-transformation-platform`
3. Right-click any `.py` file (like `main.py` or `test_poc.py`)
4. Select "Open with" → Choose a text editor:
   - **Notepad** (basic, built-in)
   - **Notepad++** (better, free download)
   - **VS Code** (best, free, recommended)
   - **Cursor** (if you have it)

### Option 2: Using Cursor (Recommended)
1. Open Cursor
2. File → Open Folder
3. Navigate to: `C:\Users\rahul\Downloads\data-transformation-platform`
4. Click "Select Folder"
5. Now you can see all files in the left sidebar
6. Click any file to open and edit it

## Understanding the Code Structure

### Main Entry Points
- **`main.py`** - Main command-line interface
  - This is what runs when you type `python main.py`
  - You can modify how it processes files here

- **`test_poc.py`** - Test script
  - Creates sample data and tests the platform
  - You can modify what test data it creates

### Core Platform Code (in `src/` folder)

**Data Ingestion** (`src/ingestion/`)
- `excel_handler.py` - How Excel files are read
- `csv_handler.py` - How CSV files are read
- `json_handler.py` - How JSON files are read
- `ppt_handler.py` - How PowerPoint files are read
- `database_handler.py` - How databases are accessed

**Data Cleaning** (`src/cleaning/`)
- `normalizer.py` - How data is normalized
- `deduplicator.py` - How duplicates are removed
- `validator.py` - How data is validated

**PII Redaction** (`src/redaction/`)
- `pii_detector.py` - How personal info is detected
- `redactor.py` - How personal info is removed/masked

**Compliance** (`src/compliance/`)
- `rules.py` - Compliance rules (GDPR, HIPAA, etc.)
- `checker.py` - How compliance is checked

**LLM Formatting** (`src/structuring/`)
- `llm_formatter.py` - How data is formatted for training

**Backend API** (`backend/`)
- `app.py` - The REST API server

## Common Edits You Might Want to Make

### 1. Change How PII is Redacted

Edit: `src/redaction/redactor.py`

Find the `_get_replacement()` function and modify it:

```python
def _get_replacement(self, entity_type: str, original_text: str) -> str:
    """Get replacement text based on strategy"""
    if self.strategy == 'mask':
        # Change this line to customize masking
        return '*' * len(original_text)  # Current: masks with asterisks
        # Or try: return '[REDACTED]'  # Alternative
```

### 2. Add a New File Format Handler

1. Create a new file: `src/ingestion/pdf_handler.py`
2. Copy the structure from `excel_handler.py`
3. Modify it to read PDF files
4. Register it in `src/ingestion/registry.py`

### 3. Change Output Format

Edit: `src/structuring/llm_formatter.py`

Find the `format_for_training()` function and modify the output structure.

### 4. Add Custom Compliance Rules

Edit: `src/compliance/rules.py`

Add new rules to the `_load_rules()` function.

### 5. Modify the Test Data

Edit: `test_poc.py`

Find the `create_sample_data()` function and change what data it creates.

## Testing Your Changes

After editing code:

1. **Save the file** (Ctrl+S)

2. **Test your changes:**
   ```bash
   python test_poc.py
   ```

3. **If you get errors:**
   - Check the error message
   - Make sure you saved the file
   - Check for typos (Python is case-sensitive!)

## Tips for Editing

1. **Always make a backup first:**
   - Copy the file before editing
   - Or use Git (see GitHub section)

2. **Edit one thing at a time:**
   - Make small changes
   - Test after each change

3. **Read the comments:**
   - Code has comments explaining what each part does
   - Start with understanding before changing

4. **Use a good editor:**
   - VS Code or Cursor show errors as you type
   - They highlight syntax
   - They help with autocomplete

## Getting Help

If you're stuck:
1. Read the error message carefully
2. Check the file path is correct
3. Make sure you saved the file
4. Try undoing your last change

## Example: Simple Edit

Let's say you want to change the output file format from JSONL to JSON:

1. Open `src/structuring/llm_formatter.py`
2. Find line with `self.output_format = self.config.get('output_format', 'jsonl')`
3. Change `'jsonl'` to `'json'`
4. Save the file
5. Run `python test_poc.py` to test

That's it! You've edited the code.

