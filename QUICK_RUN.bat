@echo off
echo ========================================
echo Process YOUR Data File
echo ========================================
echo.

echo Enter the name of your data file:
echo (Example: mydata.csv, sales.xlsx, data.json)
set /p FILENAME="File name: "

if "%FILENAME%"=="" (
    echo ERROR: No file name entered
    pause
    exit /b 1
)

echo.
echo Enter output file name (or press Enter for default):
set /p OUTPUT="Output name (default: processed.jsonl): "

if "%OUTPUT%"=="" set OUTPUT=processed.jsonl

echo.
echo Processing %FILENAME%...
echo.

python main.py --input "%FILENAME%" --output "%OUTPUT%"

if errorlevel 1 (
    echo.
    echo ERROR: Processing failed
    echo Check the error message above
    pause
    exit /b 1
)

echo.
echo ========================================
echo Processing completed!
echo Output file: %OUTPUT%
echo ========================================
echo.
pause

