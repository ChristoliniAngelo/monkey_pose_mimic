#!/bin/bash
# Monkey Pose Mimic - Linux/macOS Setup Script
# Sets up virtual environment and installs dependencies

echo "========================================"
echo "Monkey Pose Mimic - Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD=python3.12
elif command -v python3 &> /dev/null; then
    VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
    if [[ "$VERSION" == "3.12" ]]; then
        PYTHON_CMD=python3
    else
        echo "ERROR: Python 3.12 not found!"
        echo ""
        echo "Current Python version: $(python3 --version)"
        echo "Please install Python 3.12"
        echo ""
        echo "macOS: https://www.python.org/ftp/python/3.12.8/python-3.12.8-macos11.pkg"
        echo "Linux: Use your package manager (e.g., apt, dnf, pacman)"
        exit 1
    fi
else
    echo "ERROR: Python not found!"
    exit 1
fi

echo "Python 3.12 found: $($PYTHON_CMD --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Removing..."
    rm -rf venv
fi

$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment!"
    exit 1
fi

echo "Virtual environment created successfully!"
echo ""

# Activate virtual environment and install dependencies
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Upgrading pip..."
pip install --upgrade pip

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies!"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "To run the application, use: ./run.sh"
echo "Or manually:"
echo "  1. source venv/bin/activate"
echo "  2. python main.py"
echo ""
