@echo off
echo ========================================
echo Data Transformation Platform - Test
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo Step 2: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo Step 3: Installing spaCy model...
python -m spacy download en_core_web_sm
if errorlevel 1 (
    echo WARNING: spaCy model installation failed, but continuing...
)
echo.

echo Step 4: Running test...
python test_poc.py
if errorlevel 1 (
    echo ERROR: Test failed
    pause
    exit /b 1
)
echo.

echo ========================================
echo Test completed! Check test_output folder
echo ========================================
pause

