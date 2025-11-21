# Code Summary - Overview

This folder contains high-level summaries of the codebase organized by the 6 main pipeline layers.

---

## 📁 Structure

### 1. Ingestion Layer (`01_INGESTION_LAYER_SUMMARY.md`)
- Format handlers (40+ file types)
- Enterprise connectors (databases, CRM, ERP, cloud)
- Metadata extraction
- Data extraction and standardization

### 2. Cleaning Layer (`02_CLEANING_LAYER_SUMMARY.md`)
- Data normalization
- Deduplication (exact + fuzzy)
- Validation
- Pipeline orchestration

### 3. Redaction Layer (`03_REDACTION_LAYER_SUMMARY.md`)
- PII/PHI detection (Presidio + patterns)
- Data redaction (mask/remove/hash/replace)
- Entity location tracking
- Privacy protection

### 4. Compliance Layer (`04_COMPLIANCE_LAYER_SUMMARY.md`)
- Regulatory validation (GDPR, HIPAA, PCI-DSS, SOX)
- Compliance checking
- Issue identification
- Recommendations

### 5. Relationship Detection (`05_RELATIONSHIP_DETECTION_SUMMARY.md`)
- Content-based matching
- Filename pattern matching
- Metadata matching
- Relationship graph construction

### 6. Agentic AI Formatting (`06_AGENTIC_AI_FORMATTING_SUMMARY.md`)
- Multi-file context generation
- Relationship-aware formatting
- Synthetic reasoning (rule-based)
- Training prompt/completion generation

---

## 🎯 Purpose

These summaries provide:
- **High-level overview** of each layer
- **Key components** and their purposes
- **Data flow** through each layer
- **Design patterns** used
- **Output formats** and structures

**For detailed technical documentation**, see `instruction_documentation/docs/TECHNICAL.md`

---

## 📊 Pipeline Flow

```
Ingestion → Cleaning → Redaction → Compliance
                ↓
        Relationship Detection
                ↓
        Agentic AI Formatting
                ↓
            Output (JSONL)
```

---

**Each summary explains what the code does, how it works, and why it's structured that way.**

