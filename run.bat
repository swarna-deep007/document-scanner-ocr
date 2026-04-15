@echo off
REM Document Scanner & OCR - Quick Start Script for Windows
REM This script will check dependencies and help you get started

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════
echo   DOCUMENT SCANNER ^& OCR - SETUP WIZARD
echo ════════════════════════════════════════════════════════
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python from: https://www.python.org
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Python is installed
python --version

REM Check if virtual environment exists
if not exist "venv" (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✓ Virtual environment activated

REM Install dependencies
echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed

REM Run quickstart checks
echo.
python quickstart.py

echo.
echo Choose what to do:
echo.
echo 1. Start Web Interface (Recommended)
echo 2. Scan Single Document (CLI)
echo 3. Run Examples
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting Web Interface...
    echo Open your browser to: http://localhost:5000
    echo.
    python web_app.py
) else if "%choice%"=="2" (
    echo.
    set /p docpath="Enter document path: "
    python cli.py single "!docpath!"
) else if "%choice%"=="3" (
    echo.
    echo Running examples...
    python examples.py
) else (
    echo Exiting...
)

pause
