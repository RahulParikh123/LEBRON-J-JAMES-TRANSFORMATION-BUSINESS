# Cleaning Layer - Code Summary

## Overview
The Cleaning Layer normalizes, deduplicates, and validates data to ensure consistency and quality before further processing.

---

## Key Components

### 1. Cleaning Pipeline (`pipeline.py`)
**Purpose**: Orchestrates the complete cleaning process

**Processing Steps**:
1. **Normalization** - Standardize data structure and types
2. **Validation** - Check data against schemas (before deduplication)
3. **Deduplication** - Remove exact and fuzzy duplicates
4. **Final Validation** - Re-validate after cleaning

**Key Methods**:
- `clean(data, schema, key_columns)`: Runs complete cleaning pipeline
- Returns cleaned data + statistics for each step

---

### 2. Data Normalizer (`normalizer.py`)
**Purpose**: Standardizes data structure and types

**What it does**:
- **Column normalization**: Converts column names to lowercase, removes spaces, standardizes format
- **Type conversion**: Infers and converts data types (string, number, date)
- **Missing value handling**: Standardizes null/empty values
- **Format standardization**: Ensures consistent data formats

**Key Features**:
- Handles DataFrames, lists, and dictionaries
- Preserves data structure while standardizing
- Tracks all transformations applied

---

### 3. Data Deduplicator (`deduplicator.py`)
**Purpose**: Removes duplicate records

**Detection Methods**:
- **Exact matching**: Identical records
- **Fuzzy matching**: Similar records (using Levenshtein distance)
- **Key-based**: Deduplication on specific columns

**Algorithms**:
- Uses `fuzzywuzzy` for fuzzy string matching
- Uses `recordlinkage` for record linkage
- Configurable similarity threshold (default: 0.85)

**Key Features**:
- Handles large datasets efficiently
- Preserves first occurrence, removes duplicates
- Tracks number of duplicates removed

---

### 4. Data Validator (`validator.py`)
**Purpose**: Validates data against schemas and rules

**Validation Types**:
- **Schema validation**: Checks required columns, data types
- **Range validation**: Checks value ranges
- **Format validation**: Checks formats (email, phone, etc.)
- **Business rules**: Custom validation rules

**Key Features**:
- Validates before and after cleaning
- Reports all validation issues
- Provides recommendations for fixes

---

## Data Flow

```
Raw Data
    ↓
Normalization
    ├── Column name standardization
    ├── Type conversion
    └── Format standardization
    ↓
Validation (Pre-deduplication)
    ├── Schema checks
    └── Format checks
    ↓
Deduplication
    ├── Exact match removal
    └── Fuzzy match removal
    ↓
Final Validation
    ↓
Cleaned Data
```

---

## Statistics Tracked

- **Total steps**: Number of cleaning steps applied
- **Duplicates removed**: Count of duplicate records
- **Validation issues**: Number of issues found
- **Transformations applied**: List of all transformations

---

## Configuration

**Normalization**:
- Enable/disable normalization
- Custom column name mappings
- Type conversion rules

**Deduplication**:
- Similarity threshold (0.0-1.0)
- Exact match only vs fuzzy matching
- Key columns for deduplication

**Validation**:
- Schema definition
- Validation rules
- Error handling strategy

---

## Key Design Patterns

- **Pipeline Pattern**: Sequential processing through steps
- **Strategy Pattern**: Different validation/deduplication strategies
- **Template Method**: Base validation structure

---

## Output

Returns:
- **Cleaned data**: Normalized, deduplicated, validated
- **Statistics**: Detailed stats for each step
- **Issues**: List of validation issues found
- **Transformations**: All transformations applied

