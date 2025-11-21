# Enterprise Connectors

## Overview

The platform supports connections to enterprise systems including databases, CRM, ERP, and cloud storage.

---

## Database Connectors

### Supported Databases

- **PostgreSQL**
- **MySQL**
- **SQL Server (MSSQL)**
- **SQLite**
- **Oracle**
- **MongoDB**

### Connection Format

```python
# PostgreSQL
connection_string = "postgresql://user:password@host:5432/database"

# MySQL
connection_string = "mysql://user:password@host:3306/database"

# SQL Server
connection_string = "mssql://user:password@host:1433/database"

# SQLite
connection_string = "sqlite:///path/to/database.db"

# Oracle
connection_string = "oracle://user:password@host:1521/service"

# MongoDB
connection_string = "mongodb://user:password@host:27017/database"
```

### Usage

```python
from main import DataTransformationPipeline

pipeline = DataTransformationPipeline()

# Extract all tables
result = pipeline.process(
    input_path="postgresql://user:pass@host:5432/dbname",
    output_path="output/db.jsonl"
)

# Extract specific table
result = pipeline.process(
    input_path="postgresql://user:pass@host:5432/dbname",
    output_path="output/table.jsonl",
    table_name="customers"
)

# Execute custom query
result = pipeline.process(
    input_path="postgresql://user:pass@host:5432/dbname",
    output_path="output/query.jsonl",
    query="SELECT * FROM customers WHERE created_at > '2024-01-01'"
)
```

---

## CRM Connectors

### Salesforce

**Connection Format**:
```
salesforce://username:password@instance.salesforce.com
```

**Configuration**:
```python
{
    "username": "user@company.com",
    "password": "password",
    "instance": "login.salesforce.com",
    "object_type": "Account"  # Account, Contact, Opportunity, etc.
}
```

**Usage**:
```python
result = pipeline.process(
    input_path="salesforce://user:pass@instance.salesforce.com",
    output_path="output/salesforce.jsonl",
    object_type="Account"
)
```

**Supported Objects**: Account, Contact, Opportunity, Lead, Case, etc.

### HubSpot

**Connection Format**:
```
hubspot://api_key
```

**Configuration**:
```python
{
    "api_key": "your_api_key",
    "object_type": "contacts"  # contacts, companies, deals, etc.
}
```

**Usage**:
```python
result = pipeline.process(
    input_path="hubspot://api_key",
    output_path="output/hubspot.jsonl",
    object_type="contacts"
)
```

### Microsoft Dynamics CRM

**Connection Format**:
```
dynamics://instance.crm.dynamics.com
```

**Configuration**:
```python
{
    "instance": "yourinstance.crm.dynamics.com",
    "entity": "accounts"  # accounts, contacts, opportunities, etc.
}
```

**Usage**:
```python
result = pipeline.process(
    input_path="dynamics://instance.crm.dynamics.com",
    output_path="output/dynamics.jsonl",
    entity="accounts"
)
```

---

## ERP Connectors

### SAP

**Connection Format**:
```
sap://host:port
```

**Configuration**:
```python
{
    "host": "sap_server",
    "port": 8000,
    "table": "MARA"  # Material master, etc.
}
```

**Usage**:
```python
result = pipeline.process(
    input_path="sap://host:port",
    output_path="output/sap.jsonl",
    table="MARA"
)
```

**Connection Methods**:
- ODBC connection
- RFC connection
- OData API

### Oracle ERP

**Connection Format**:
```
oracleerp://host:port
```

**Configuration**:
```python
{
    "module": "Financials"  # Financials, Supply Chain, HR, etc.
}
```

**Usage**:
```python
result = pipeline.process(
    input_path="oracleerp://host:port",
    output_path="output/oracle_erp.jsonl",
    module="Financials"
)
```

### NetSuite

**Connection Format**:
```
netsuite://account_id
```

**Configuration**:
```python
{
    "account_id": "your_account",
    "record_type": "customer"  # customer, vendor, item, etc.
}
```

**Usage**:
```python
result = pipeline.process(
    input_path="netsuite://account_id",
    output_path="output/netsuite.jsonl",
    record_type="customer"
)
```

---

## Cloud Storage Connectors

### Microsoft OneDrive/SharePoint

**Connection Format**:
```
onedrive://tenant_id
```

**Configuration**:
```python
{
    "tenant_id": "your_tenant",
    "client_id": "your_client_id",
    "client_secret": "your_secret",
    "folder_path": "/Documents"
}
```

**Usage**:
```python
result = pipeline.process(
    input_path="onedrive://tenant_id",
    output_path="output/onedrive.jsonl",
    folder_path="/Documents"
)
```

**Authentication**: Uses Microsoft Graph API with OAuth 2.0

### Google Drive

**Connection Format**:
```
googledrive://project_id
```

**Configuration**:
```python
{
    "credentials_path": "path/to/credentials.json",
    "folder_id": "folder_id_here"
}
```

**Usage**:
```python
result = pipeline.process(
    input_path="googledrive://project_id",
    output_path="output/googledrive.jsonl",
    folder_id="folder_id"
)
```

**Authentication**: Uses Google API with service account credentials

---

## Environment Variables

Set up credentials in `.env` file:

```bash
# Salesforce
SALESFORCE_USERNAME=user@company.com
SALESFORCE_PASSWORD=password
SALESFORCE_INSTANCE=login.salesforce.com

# HubSpot
HUBSPOT_API_KEY=your_api_key

# Microsoft Graph
MS_TENANT_ID=your_tenant_id
MS_CLIENT_ID=your_client_id
MS_CLIENT_SECRET=your_secret

# Google Drive
GOOGLE_CREDENTIALS_PATH=path/to/credentials.json
```

---

## Authentication

### API Keys
- HubSpot: Get from HubSpot account settings
- Google Drive: Create service account in Google Cloud Console

### OAuth
- Salesforce: Username/password or OAuth 2.0
- Microsoft Graph: OAuth 2.0 with client credentials
- Google Drive: Service account JSON key

### Database
- Standard SQL connection strings
- MongoDB connection strings

---

## Error Handling

Connectors handle:
- Connection failures
- Authentication errors
- Rate limiting
- Timeout errors
- Data format errors

All errors are logged and processing continues with other files.

---

## Performance

- **Parallel Connections**: Multiple connections processed simultaneously
- **Batch Extraction**: Large datasets extracted in batches
- **Caching**: Connection metadata cached
- **Resume**: Can resume interrupted extractions

---

## Security

- **Credentials**: Never hardcoded, use environment variables
- **Encryption**: All connections use encrypted protocols
- **Access Control**: Respects system-level permissions
- **Audit Logging**: All connections logged

---

For implementation details, see [Technical Documentation](TECHNICAL.md).

