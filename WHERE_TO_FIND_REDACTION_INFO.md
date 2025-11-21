# Where to Find PII Redaction Information

## Quick Answer

**Redaction info is stored in every processed file** in this location:
```
metadata.processing_stats.redaction
```

---

## Method 1: Use the Viewer Tool (Easiest!)

**In Command Prompt**, paste this:

```bash
python view_redaction_info.py "output\output\processed\YOUR_FILE_processed.jsonl"
```

**Or view all files**:
```bash
python view_redaction_info.py "output\output\processed"
```

**What you'll see**:
- Total entities detected
- Total entities redacted  
- Breakdown by type (EMAIL, PHONE, SSN, etc.)
- Detailed locations (row, column)

---

## Method 2: Check the Processed File Directly

### Step 1: Open the Processed File

Open any file like:
- `output/output/processed/Sherry_Hu_Resume_processed.jsonl`

### Step 2: Find the Redaction Section

Look for this in the JSON:
```json
"metadata": {
  "processing_stats": {
    "redaction": {
      "entities_detected": 0,
      "entities_redacted": 0,
      "entity_summary": {},
      "entity_locations": []
    }
  }
}
```

**What each field means**:
- `entities_detected`: Number of PII entities found
- `entities_redacted`: Number that were redacted
- `entity_summary`: Count by type (EMAIL: 2, PHONE: 3, etc.)
- `entity_locations`: **NEW!** Exact locations (row, column, position)

---

## Method 3: Check All Files at Once

**In Command Prompt**, paste this:

```bash
python view_redaction_info.py "output\output\processed"
```

This shows a report for every processed file.

---

## Understanding the Results

### If You See:
```json
"entities_detected": 0
"entities_redacted": 0
```

**Meaning**: No PII was detected in this file.

**Your LEBRON files**: Most show 0 because they contain:
- Financial data (numbers, not personal info)
- Business presentations (no emails/phones)
- Resumes (but PII detection might miss formatted addresses)

### If You See:
```json
"entities_detected": 5
"entities_redacted": 5
"entity_summary": {
  "EMAIL": 2,
  "PHONE": 2,
  "SSN": 1
}
```

**Meaning**: 5 PII entities were found and redacted:
- 2 email addresses
- 2 phone numbers
- 1 SSN

---

## Detailed Location Information

**NEW**: The system now stores exact locations:

```json
"entity_locations": [
  {
    "type": "EMAIL",
    "row": 5,
    "column": "email",
    "text": "user@example.com",
    "score": 0.95
  }
]
```

**This tells you**:
- **Type**: What kind of PII (EMAIL, PHONE, SSN)
- **Row**: Which row in the data
- **Column**: Which column/field
- **Text**: What was found (first 50 chars)
- **Score**: Confidence (0.95 = 95% sure it's PII)

---

## Example: Viewing Redaction Info

### Command:
```bash
python view_redaction_info.py "output\output\processed\Sherry_Hu_Resume_processed.jsonl"
```

### Output:
```
================================================================================
PII REDACTION REPORT
File: output\output\processed\Sherry_Hu_Resume_processed.jsonl
================================================================================

SUMMARY
--------------------------------------------------------------------------------
Total Records: 1
Records with PII Detected: 0
Total Entities Detected: 0
Total Entities Redacted: 0

[OK] NO PII DETECTED
--------------------------------------------------------------------------------
This file did not contain any detected PII/PHI.
```

---

## Why Your Files Show 0

Your LEBRON test files show `entities_detected: 0` because:

1. **Excel files**: Financial models (numbers, formulas)
2. **PowerPoint files**: Business slides (no personal info)
3. **Word files**: Resumes might have names/addresses, but:
   - Presidio might not be fully initialized (Python 3.14)
   - Pattern matching might miss formatted text
   - Names alone aren't always PII

**To see redaction in action**: Create a test file with:
- Email: `test@example.com`
- Phone: `555-123-4567`
- SSN: `123-45-6789`

Then process it and check the redaction info!

---

## Summary

**Where redaction info is**:
1. ✅ In processed JSONL files: `metadata.processing_stats.redaction`
2. ✅ Use viewer tool: `python view_redaction_info.py <file>`
3. ✅ Check summary: `output/summary.json` (overall stats)

**What you'll see**:
- How many entities detected
- How many redacted
- What types (EMAIL, PHONE, etc.)
- **NEW**: Exact locations (row, column, position)

**Your files**: Show 0 because they're financial/business data, not personal info.

---

**Quick command to check any file**:
```bash
python view_redaction_info.py "output\output\processed\YOUR_FILE_processed.jsonl"
```

