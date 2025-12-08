@echo off
REM Monkey Pose Mimic - Windows Setup Script
REM Sets up virtual environment and installs dependencies

echo ========================================
echo Monkey Pose Mimic - Setup
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3.12 not found!
    echo.
    echo Please install Python 3.12 from:
    echo https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe
    echo.
    pause
    exit /b 1
)

echo Python 3.12 found!
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Removing...
    rmdir /s /q venv
)

py -3.12 -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment!
    pause
    exit /b 1
)

echo Virtual environment created successfully!
echo.

REM Activate virtual environment and install dependencies
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run the application, use: run.bat
echo Or manually:
echo   1. venv\Scripts\activate.bat
echo   2. python main.py
echo.
pause
