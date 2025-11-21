@echo off
cd /d "%~dp0"
echo ========================================
echo Processing YOUR File: HOME Model v4.xlsx
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)
python --version
echo.

echo Step 2: Checking if file exists...
if not exist "HOME Model v4.xlsx" (
    echo ERROR: File "HOME Model v4.xlsx" not found in current directory
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)
echo File found!
echo.

echo Step 3: Processing your Excel file...
echo This will:
echo   1. Read the Excel file
echo   2. Clean and normalize the data
echo   3. Remove/mask personal information
echo   4. Check compliance
echo   5. Format for LLM training
echo.
echo Please wait, this may take a minute...
echo.

python main.py --input "HOME Model v4.xlsx" --output "HOME_Model_processed.jsonl"

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Processing failed
    echo ========================================
    echo.
    echo Common issues:
    echo   1. Dependencies not installed - run: pip install -r requirements.txt
    echo   2. File is open in Excel - close it and try again
    echo   3. File format issue - check the error above
    echo.
    echo Check the error message above for details
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Processing completed!
echo ========================================
echo.

if exist "output\HOME_Model_processed.jsonl" (
    echo Output file created successfully!
    echo Location: output\HOME_Model_processed.jsonl
    echo.
    echo Opening output folder...
    start output
) else if exist "HOME_Model_processed.jsonl" (
    echo Output file created in current directory!
    echo Location: HOME_Model_processed.jsonl
) else (
    echo WARNING: Output file not found where expected
    echo Check the current directory for output files
)

echo.
echo This file is ready for LLM training!
echo ========================================
echo.
pause

