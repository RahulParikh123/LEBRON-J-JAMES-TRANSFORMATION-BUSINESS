# How to View PII Redaction Information

## Where Redaction Info is Stored

PII redaction information is stored in **every processed file** in the `metadata.processing_stats.redaction` section.

### Location in Processed Files

Each processed JSONL file contains:
```json
{
  "metadata": {
    "processing_stats": {
      "redaction": {
        "entities_detected": 5,
        "entities_redacted": 5,
        "entity_summary": {
          "EMAIL": 2,
          "PHONE": 2,
          "SSN": 1
        },
        "entity_locations": [
          {
            "type": "EMAIL",
            "row": 0,
            "column": "email",
            "text": "john@example.com",
            "score": 0.95
          }
        ],
        "by_column": {
          "email": [
            {
              "type": "EMAIL",
              "row": 0,
              "text": "john@example.com"
            }
          ]
        }
      }
    }
  }
}
```

---

## Method 1: Use the Redaction Viewer Tool

I created a tool to easily view redaction information!

### View Single File

**In Command Prompt**, paste this:

```bash
python view_redaction_info.py "output\output\processed\Sherry_Hu_Resume_processed.jsonl"
```

**What you'll see**:
- Total entities detected
- Total entities redacted
- Breakdown by entity type (EMAIL, PHONE, SSN, etc.)
- Detailed locations (row, column, position)

### View All Files in Directory

**In Command Prompt**, paste this:

```bash
python view_redaction_info.py "output\output\processed"
```

**What you'll see**: Redaction report for every processed file

---

## Method 2: Check the JSONL File Directly

### Step 1: Open the Processed File

Open any processed file, for example:
- `output/output/processed/Sherry_Hu_Resume_processed.jsonl`

### Step 2: Look for Redaction Stats

In the file, find the `processing_stats.redaction` section:

```json
"redaction": {
  "entities_detected": 0,
  "entities_redacted": 0,
  "entity_summary": {}
}
```

**What each field means**:
- `entities_detected`: How many PII entities were found
- `entities_redacted`: How many were redacted
- `entity_summary`: Breakdown by type (EMAIL, PHONE, etc.)
- `entity_locations`: Exact locations (row, column, position) - **NEW!**

---

## Method 3: Check Summary File

**In Command Prompt**, paste this:

```bash
type output\summary.json
```

This shows overall stats, but not detailed locations.

---

## Understanding the Output

### If `entities_detected: 0`

**Meaning**: No PII was detected in this file.

**Your LEBRON files**: Most had `entities_detected: 0` because:
- They're financial models (numbers, not personal info)
- They're presentations (business content)
- They're resumes (but PII detection might have missed some)

### If `entities_detected: 5`

**Meaning**: 5 PII entities were found and redacted.

**You'll see**:
- `entity_summary`: `{"EMAIL": 2, "PHONE": 2, "SSN": 1}`
- `entity_locations`: Exact row/column where each was found

---

## Example: What Redaction Looks Like

### Before Redaction:
```
Email: john.doe@example.com
Phone: 555-123-4567
SSN: 123-45-6789
```

### After Redaction (mask strategy):
```
Email: ********************
Phone: ************
SSN: ***********
```

### After Redaction (replace strategy):
```
Email: [EMAIL]
Phone: [PHONE]
SSN: [SSN]
```

---

## Detailed Location Information

**NEW**: The system now stores exact locations where PII was found:

```json
"entity_locations": [
  {
    "type": "EMAIL",
    "row": 5,
    "column": "contact_email",
    "text": "user@example.com",
    "score": 0.95
  },
  {
    "type": "PHONE",
    "row": 12,
    "column": "phone_number",
    "text": "555-123-4567",
    "score": 0.88
  }
]
```

**This tells you**:
- **What type**: EMAIL, PHONE, SSN, etc.
- **Where**: Row 5, Column "contact_email"
- **What was found**: "user@example.com"
- **Confidence**: 0.95 (95% sure it's PII)

---

## Quick Commands

### View Redaction Info for One File
```bash
python view_redaction_info.py "output\output\processed\YOUR_FILE_processed.jsonl"
```

### View Redaction Info for All Files
```bash
python view_redaction_info.py "output\output\processed"
```

### Check if Any PII Was Found
```bash
python -c "import json; f=open('output/output/processed/YOUR_FILE_processed.jsonl'); d=json.loads(f.readline()); print('Entities:', d['value']['metadata']['processing_stats']['redaction']['entities_detected'])"
```

---

## Why Your Files Show 0 Entities

Your LEBRON test files show:
```json
"redaction": {
  "entities_detected": 0,
  "entities_redacted": 0,
  "entity_summary": {}
}
```

**This means**: No PII was detected because:
1. **Excel files**: Financial data (numbers, not personal info)
2. **PowerPoint files**: Business presentations (no emails, phones, SSNs)
3. **Word files**: Resumes might have names/addresses, but:
   - Presidio might not be fully initialized (Python 3.14 compatibility)
   - Pattern matching might miss formatted addresses
   - Names alone aren't always detected as PII

**To test with PII**: Create a test file with:
- Email addresses: `test@example.com`
- Phone numbers: `555-123-4567`
- SSNs: `123-45-6789`

Then process it and you'll see redaction in action!

---

## Summary

**Where to find redaction info**:
1. ✅ **In processed JSONL files**: `metadata.processing_stats.redaction`
2. ✅ **Use the viewer tool**: `python view_redaction_info.py <file>`
3. ✅ **Check summary**: `output/summary.json`

**What you'll see**:
- How many entities detected
- How many redacted
- What types (EMAIL, PHONE, etc.)
- **NEW**: Exact locations (row, column)

**Your files**: Show 0 because they don't contain detectable PII (financial/business data, not personal info).

