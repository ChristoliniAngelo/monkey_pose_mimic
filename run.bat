@echo off
REM Monkey Pose Mimic - Windows Run Script
REM Activates virtual environment and runs the application

echo ========================================
echo Monkey Pose Mimic - Starting...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Run the application
echo Starting Monkey Pose Mimic...
echo.
python main.py

REM Deactivate on exit
deactivate

echo.
echo Application closed.
pause
