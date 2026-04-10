#!/usr/bin/env bash
# MSPP Data Plotter - Desktop Launcher (Development Mode)
# Run this script to launch the app in development mode with debugging enabled
# chmod +x Launch_MSPP_App.sh && ./Launch_MSPP_App.sh

set -e  # Exit on error

# Navigate to project directory (from scripts/launch, go up 2 levels)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

# Verify we're in the correct directory
if [ ! -f "scripts/launch/web_launcher.py" ]; then
    echo ""
    echo "ERROR: Could not find web_launcher.py!"
    echo ""
    echo "Expected: $(pwd)/scripts/launch/web_launcher.py"
    echo ""
    echo "This usually means the script was moved or the path is incorrect."
    echo ""
    exit 1
fi

echo "==============================================================="
echo "Starting MSPP Data Plotter (Development Mode)"
echo "==============================================================="
echo ""

# Find Python executable - try venv first, then system
PYTHON_EXE=""
PYTHON_SOURCE=""

if [ -f ".venv/bin/python3" ]; then
    PYTHON_EXE=".venv/bin/python3"
    PYTHON_SOURCE="virtual environment (.venv)"
elif [ -f ".venv/bin/python" ]; then
    PYTHON_EXE=".venv/bin/python"
    PYTHON_SOURCE="virtual environment (.venv)"
elif [ -f ".pixi/envs/default/bin/python" ]; then
    PYTHON_EXE=".pixi/envs/default/bin/python"
    PYTHON_SOURCE="pixi environment (.pixi/envs/default)"
elif command -v python3 &> /dev/null; then
    PYTHON_EXE="python3"
    PYTHON_SOURCE="system Python3"
elif command -v python &> /dev/null; then
    PYTHON_EXE="python"
    PYTHON_SOURCE="system Python"
else
    echo ""
    echo "ERROR: Python not found or not properly installed!"
    echo ""
    echo "To fix this, run one of these setup commands:"
    echo ""
    echo "Option 1 - Automated Setup (Recommended):"
    echo "  bash scripts/setup_dev.sh"
    echo ""
    echo "Option 2 - Python Setup Tool:"
    echo "  python scripts/setup_dev.py"
    echo ""
    echo "Option 3 - PowerShell Setup (Windows/WSL):"
    echo "  ./scripts/setup_dev.ps1"
    echo ""
    echo "If you don't have Python installed:"
    echo "  Download from: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

echo "Using Python from: $PYTHON_SOURCE"
echo ""
echo "Project Root: $(pwd)"
echo ""

# Verify Python works by checking version
if ! "$PYTHON_EXE" --version &> /dev/null; then
    echo ""
    echo "ERROR: Python found but not working properly"
    echo "Path: $PYTHON_EXE"
    echo ""
    echo "Try reinstalling Python or running the setup script:"
    echo "  bash scripts/setup_dev.sh"
    echo ""
    exit 1
fi

echo ""

# Set development environment variables
export FLASK_ENV=development
export FLASK_HOST=127.0.0.1
export FLASK_PORT=5000

echo "Attempting to launch: $(pwd)/scripts/launch/web_launcher.py"
echo ""

# Run the launcher
"$PYTHON_EXE" "$(pwd)/scripts/launch/web_launcher.py"

EXIT_CODE=$?
echo ""
echo "App terminated with exit code: $EXIT_CODE"
