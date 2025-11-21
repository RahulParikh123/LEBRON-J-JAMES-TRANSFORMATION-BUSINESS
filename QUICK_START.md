# Quick Start Guide

Get up and running with the LEBRON-J'JAMES-TRANSFORMATION-BUSINESS platform in minutes.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/LEBRON-J-JAMES-TRANSFORMATION-BUSINESS.git
cd LEBRON-J-JAMES-TRANSFORMATION-BUSINESS
```

### 2. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Optional: For better PDF extraction
pip install pdfplumber

# Optional: For image OCR
pip install pytesseract
```

### 3. Verify Installation

```bash
python -c "from src.ingestion.registry import FormatRegistry; r = FormatRegistry(); print(f'Registered {len(r._handlers)} handlers')"
```

You should see: `Registered 18 handlers`

---

## 📝 Basic Usage

### Process a Single File

```python
from main import DataTransformationPipeline

pipeline = DataTransformationPipeline()
result = pipeline.process(
    input_path="path/to/file.xlsx",
    output_path="output/processed.jsonl"
)

print(f"Status: {result['status']}")
print(f"Output: {result['output_path']}")
```

### Process a Directory (Batch)

```bash
python test_batch.py --dir "YOUR_DATA_FOLDER"
```

This will:
- ✅ Scan directory for all supported files
- ✅ Process files in parallel
- ✅ Extract metadata and relationships
- ✅ Generate training data
- ✅ Save results to `output/` folder

---

## 📊 Check Results

After processing, check the output:

```bash
# View summary
cat output/summary.json

# View relationships
cat output/relationships/relationship_graph.json

# View training data
head -n 5 output/agentic_ai/training_data.jsonl
```

---

## 🎯 Example: Process Sample Files

The repository includes sample files in `samples/`:

```bash
# Process the sample files
python test_batch.py --dir "samples"
```

You'll see:
- Input files: Excel, Word, PowerPoint
- Processed outputs: JSONL files with transformed data

---

## 🔧 Configuration

### Environment Variables

Create `.env` file for enterprise systems:

```bash
# Salesforce
SALESFORCE_USERNAME=user@company.com
SALESFORCE_PASSWORD=password

# HubSpot
HUBSPOT_API_KEY=your_api_key
```

### Config File

Create `config.yaml`:

```yaml
batch:
  max_workers: 4
  chunk_size: 100

relationships:
  min_confidence: 0.7
```

---

## 📚 Next Steps

1. **Try the samples**: Process files in `samples/` directory
2. **Read the docs**: Check `docs/` folder for detailed documentation
3. **Process your data**: Use your own files
4. **Connect enterprise systems**: Configure CRM/ERP connectors

---

## 🆘 Troubleshooting

### Import Errors

```bash
# Make sure you're in the project directory
cd LEBRON-J-JAMES-TRANSFORMATION-BUSINESS

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### File Not Found

```bash
# Check file path
python -c "from pathlib import Path; print(Path('YOUR_FILE').exists())"
```

### Permission Errors

```bash
# On Windows, run as administrator if needed
# On Linux/Mac, check file permissions
chmod +x test_batch.py
```

---

## 📖 Documentation

- **[README.md](README.md)** - Overview
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[docs/TECHNICAL.md](docs/TECHNICAL.md)** - Technical details
- **[docs/COMPONENTS.md](docs/COMPONENTS.md)** - Component guide

---

**You're ready to start transforming data!** 🎉

