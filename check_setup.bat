@echo off
cd /d "%~dp0"
echo ========================================
echo Setup Checker
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is NOT installed or not in PATH
    echo.
    echo ACTION REQUIRED:
    echo   1. Go to: https://www.python.org/downloads/
    echo   2. Download and install Python
    echo   3. Make sure to check "Add Python to PATH"
    echo   4. Restart your computer
    echo   5. Run this check again
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo [OK] Python is installed
)
echo.

echo Checking if your file exists...
if exist "HOME Model v4.xlsx" (
    echo [OK] File found: HOME Model v4.xlsx
) else (
    echo [X] File not found: HOME Model v4.xlsx
    echo      Make sure the file is in this folder
)
echo.

echo Checking dependencies...
python -c "import pandas" >nul 2>&1
if errorlevel 1 (
    echo [X] Dependencies are NOT installed
    echo.
    echo ACTION REQUIRED:
    echo   Run: pip install -r requirements.txt
    echo   (This will take 5-10 minutes)
) else (
    echo [OK] Dependencies are installed
)
echo.

echo Checking language model...
python -c "import spacy; spacy.load('en_core_web_sm')" >nul 2>&1
if errorlevel 1 (
    echo [X] Language model is NOT installed
    echo.
    echo ACTION REQUIRED:
    echo   Run: python -m spacy download en_core_web_sm
) else (
    echo [OK] Language model is installed
)
echo.

echo ========================================
echo Setup Check Complete
echo ========================================
echo.
echo If all checks show [OK], you're ready to go!
echo If any show [X], follow the ACTION REQUIRED steps above.
echo.
pause

