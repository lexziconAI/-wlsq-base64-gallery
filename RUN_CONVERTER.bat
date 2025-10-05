@echo off
REM WLSQ Assets Converter - Quick Run
REM Double-click this file to run the conversion

echo ========================================
echo WLSQ Assets Base64 Converter
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from python.org
    echo.
    pause
    exit /b 1
)

echo Running conversion...
echo.

python convert_wlsq_assets.py

echo.
echo ========================================
echo Conversion complete!
echo ========================================
echo.
pause
