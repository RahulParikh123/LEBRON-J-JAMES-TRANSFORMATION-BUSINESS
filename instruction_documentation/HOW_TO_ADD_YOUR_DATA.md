# How to Add YOUR Data File

## Important: "YOUR_FILE.csv" is Just an Example!

**"YOUR_FILE.csv" is NOT a real file** - it's just a placeholder showing you where to put YOUR actual file name.

## What You Need to Do

### Step 1: Get Your Data File Ready

You need to have a data file somewhere on your computer. It could be:
- A CSV file (`.csv`)
- An Excel file (`.xlsx` or `.xls`)
- A JSON file (`.json`)
- A PowerPoint file (`.pptx`)

**Where is your data file?**
- On your Desktop?
- In Downloads?
- In Documents?
- Somewhere else?

### Step 2: Copy Your File to the Project Folder

1. **Open File Explorer**
2. **Find your data file** (wherever it is on your computer)
3. **Copy it** (Right-click → Copy, or Ctrl+C)
4. **Go to:** `C:\Users\rahul\Downloads\data-transformation-platform`
5. **Paste it** (Right-click → Paste, or Ctrl+V)

**OR** you can drag and drop:
1. Open File Explorer
2. Find your data file
3. Drag it into the project folder

### Step 3: Note the Exact File Name

After copying, note the **exact name** of your file, including the extension:
- `customers.csv`
- `sales_data.xlsx`
- `products.json`
- etc.

### Step 4: Run the Command

Open Command Prompt and type:

```bash
cd C:\Users\rahul\Downloads\data-transformation-platform
python main.py --input YOUR_ACTUAL_FILENAME.csv --output processed.jsonl
```

**Replace `YOUR_ACTUAL_FILENAME.csv` with your real file name!**

## Examples

### Example 1: If your file is called "customers.csv"
```bash
python main.py --input customers.csv --output processed.jsonl
```

### Example 2: If your file is called "sales_data.xlsx"
```bash
python main.py --input sales_data.xlsx --output processed.jsonl
```

### Example 3: If your file is called "mydata.json"
```bash
python main.py --input mydata.json --output processed.jsonl
```

## Easier Way: Use QUICK_RUN.bat

1. **Copy your data file** to the project folder (Step 2 above)
2. **Double-click** `QUICK_RUN.bat`
3. **Type your file name** when it asks (just the name, like `customers.csv`)
4. **Press Enter**

It will do everything for you!

## What If You Don't Have a Data File Yet?

### Option 1: Test with Sample Data First

Run this to create sample data and test the platform:

```bash
python test_poc.py
```

This creates sample files and processes them so you can see how it works.

### Option 2: Create a Test File

1. Open Excel or Google Sheets
2. Create a simple table with some data
3. Save it as CSV
4. Copy it to your project folder
5. Run the command with that file name

## Quick Checklist

- [ ] I have a data file (CSV, Excel, JSON, etc.)
- [ ] I copied it to the project folder
- [ ] I know the exact file name
- [ ] I'm ready to run the command

## Still Confused?

**Think of it like this:**
- The command is like a recipe
- "YOUR_FILE.csv" is like saying "add your ingredient here"
- You need to replace it with YOUR actual ingredient (file name)

**Example:**
- Recipe says: "Add YOUR_INGREDIENT"
- You have: "chocolate"
- You do: "Add chocolate"

Same thing:
- Command says: `--input YOUR_FILE.csv`
- You have: `customers.csv`
- You do: `--input customers.csv`

## Summary

1. **"YOUR_FILE.csv" is NOT a real file** - it's just an example
2. **You need to ADD your own data file** to the project folder
3. **Then use YOUR file's actual name** in the command
4. **Or use QUICK_RUN.bat** - it's easier!

