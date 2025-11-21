# Redaction Layer - Code Summary

## Overview
The Redaction Layer detects and redacts PII/PHI (Personally Identifiable Information / Protected Health Information) from data to ensure privacy and compliance.

---

## Key Components

### 1. Redaction Pipeline (`pipeline.py`)
**Purpose**: Orchestrates PII detection and redaction

**Processing Steps**:
1. **Detection** - Identify PII/PHI entities in data
2. **Redaction** - Remove or mask detected entities (if not detect-only mode)

**Key Methods**:
- `process(data, entity_types, columns, detect_only)`: Complete detection + redaction
- Returns processed data + detection statistics

---

### 2. PII Detector (`pii_detector.py`)
**Purpose**: Detects PII/PHI entities in data

**Detection Methods**:

**1. Presidio (ML-based)**:
- Uses Microsoft Presidio Analyzer
- ML models for entity recognition
- Detects: names, emails, phones, SSNs, credit cards, locations, etc.
- Provides confidence scores

**2. Custom Pattern Matching**:
- Regex patterns for common PII types
- Patterns for: SSN, credit cards, IP addresses, phones, emails
- Fallback when Presidio unavailable

**Detection Types**:
- `EMAIL`: Email addresses
- `PHONE`: Phone numbers
- `SSN`: Social Security Numbers
- `CREDIT_CARD`: Credit card numbers
- `PERSON`: Person names
- `IP_ADDRESS`: IP addresses
- And more...

**Key Methods**:
- `detect(data, entity_types)`: Detects PII in data
- Returns list of entities with locations (row, column, position)

**Output Format**:
```python
{
    'entities': [
        {
            'type': 'EMAIL',
            'start': 10,
            'end': 25,
            'text': 'user@example.com',
            'score': 0.95,
            'row': 5,
            'column': 'email'
        }
    ],
    'count': 5,
    'summary': {'EMAIL': 2, 'PHONE': 3}
}
```

---

### 3. Data Redactor (`redactor.py`)
**Purpose**: Redacts detected PII/PHI from data

**Redaction Strategies**:

**1. Mask** (default):
- Replaces PII with asterisks
- Preserves length: `user@example.com` → `*******************`

**2. Remove**:
- Deletes PII entirely
- Leaves empty string

**3. Hash**:
- Replaces with SHA256 hash (first 8 chars)
- Example: `user@example.com` → `a1b2c3d4`

**4. Replace**:
- Replaces with placeholder
- Example: `[EMAIL]`, `[PHONE]`, `[SSN]`

**Key Methods**:
- `redact(data, entity_types, columns)`: Redacts PII from data
- Handles DataFrames, lists, strings
- Tracks statistics (entities redacted, rows modified)

---

## Data Flow

```
Data with PII
    ↓
PII Detection
    ├── Presidio (ML-based)
    └── Custom patterns
    ↓
Entity List (with locations)
    ↓
Redaction (if not detect-only)
    ├── Mask/Remove/Hash/Replace
    └── Apply to detected locations
    ↓
Redacted Data
```

---

## Statistics Tracked

- **Entities detected**: Total number of PII entities found
- **Entities redacted**: Number successfully redacted
- **Entity summary**: Breakdown by type (EMAIL: 5, PHONE: 3, etc.)
- **Entity locations**: Exact locations (row, column, position) - **NEW!**

---

## Configuration

**Detection**:
- Entity types to detect (all or specific)
- Confidence threshold
- Use Presidio vs patterns only

**Redaction**:
- Strategy: mask, remove, hash, replace
- Entity types to redact
- Specific columns to redact

---

## Key Design Patterns

- **Strategy Pattern**: Different redaction strategies
- **Template Method**: Base detection/redaction structure
- **Chain of Responsibility**: Multiple detection methods

---

## Output

Returns:
- **Processed data**: Data with PII redacted
- **Detection results**: All entities found with locations
- **Statistics**: Counts, summaries, locations
- **Original data**: Preserved for comparison

---

## Privacy & Security

- **No logging of PII**: Sensitive data never logged
- **Secure redaction**: Multiple strategies available
- **Location tracking**: Know exactly where PII was found
- **Compliance-ready**: Output ready for regulatory requirements

