#!/usr/bin/env bash
# MSPP Data Plotter - Desktop Launcher (Development Mode)
# Run this script to launch the app in development mode with debugging enabled
# chmod +x Launch_MSPP_App.sh && ./Launch_MSPP_App.sh

set -e  # Exit on error

# Navigate to project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==============================================================="
echo "Starting MSPP Data Plotter (Development Mode)"
echo "==============================================================="
echo ""

# Find Python executable - try venv first, then system
PYTHON_EXE="python3"

if [ -f ".venv/bin/python3" ]; then
    PYTHON_EXE=".venv/bin/python3"
    echo "Using virtual environment: .venv"
elif [ -f ".venv/bin/python" ]; then
    PYTHON_EXE=".venv/bin/python"
    echo "Using virtual environment: .venv"
elif command -v python3 &> /dev/null; then
    PYTHON_EXE="python3"
    echo "Using system Python3"
elif command -v python &> /dev/null; then
    PYTHON_EXE="python"
    echo "Using system Python"
else
    echo "ERROR: Python not found. Please install Python 3.10+"
    exit 1
fi

echo ""

# Set development environment variables
export FLASK_ENV=development
export FLASK_HOST=127.0.0.1
export FLASK_PORT=5000

echo "Launching web app on http://localhost:5000"
echo ""

# Run the launcher
"$PYTHON_EXE" programs/mspp_web/launch_app.py

echo ""
echo "App terminated."
