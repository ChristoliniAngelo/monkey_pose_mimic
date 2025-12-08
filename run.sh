#!/bin/bash
# Monkey Pose Mimic - Linux/macOS Run Script
# Activates virtual environment and runs the application

echo "========================================"
echo "Monkey Pose Mimic - Starting..."
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run ./setup.sh first to set up the environment."
    echo ""
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run the application
echo "Starting Monkey Pose Mimic..."
echo ""
python main.py

# Deactivate on exit
deactivate

echo ""
echo "Application closed."
