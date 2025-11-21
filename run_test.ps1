# PowerShell script to run the test
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Data Transformation Platform - Test" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

Write-Host "Step 2: Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Installing spaCy model..." -ForegroundColor Yellow
python -m spacy download en_core_web_sm
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ WARNING: spaCy model installation failed, but continuing..." -ForegroundColor Yellow
}
Write-Host ""

Write-Host "Step 4: Running test..." -ForegroundColor Yellow
python test_poc.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ ERROR: Test failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Test completed! Check test_output folder" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"

