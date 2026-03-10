#!/usr/bin/env bash
# MSPP Data Plotter - Desktop Launcher (Production Mode)
# Run this script to launch the app in production mode (optimized performance, no debugging)
# chmod +x Launch_MSPP_App_Prod.sh && ./Launch_MSPP_App_Prod.sh

set -e  # Exit on error

# Navigate to project directory (from scripts/launch, go up 2 levels)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/../.."

# Verify we're in the correct directory
if [ ! -f "scripts/launch/launcher.py" ]; then
    echo ""
    echo "ERROR: Could not find launcher.py!"
    echo ""
    echo "Expected: $(pwd)/scripts/launch/launcher.py"
    echo ""
    echo "This usually means the script was moved or the path is incorrect."
    echo ""
    exit 1
fi

echo "==============================================================="
echo "Starting MSPP Data Plotter (Production Mode)"
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

# Set production environment variables (no debugging, optimized)
export FLASK_ENV=production
export FLASK_HOST=127.0.0.1
export FLASK_PORT=5000

echo "Attempting to launch: $(pwd)/scripts/launch/launcher.py --prod"
echo ""

# Run the launcher
"$PYTHON_EXE" "scripts/launch/launcher.py" --prod

EXIT_CODE=$?
echo ""
echo "App terminated with exit code: $EXIT_CODE"
