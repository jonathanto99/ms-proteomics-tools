#!/usr/bin/env bash
# Quick setup script for new developers (macOS/Linux)
# Run: chmod +x ./scripts/setup_dev.sh && ./scripts/setup_dev.sh

set -e  # Exit on error

echo "🔬 BYU MS Core Lab - Development Environment Setup"
echo "=================================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1)
if [[ $PYTHON_VERSION =~ Python\ 3\.1[0-4] ]]; then
    echo "✅ $PYTHON_VERSION detected"
else
    echo "⚠️  Python 3.10+ recommended. Found: $PYTHON_VERSION"
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip --quiet

# Install Python dependencies
echo ""
echo "📥 Installing Python dependencies (including dev tools)..."
pip install -e ".[dev]" --quiet
echo "✅ Python dependencies installed"

# Summary
echo ""
echo "=================================================="
echo "✨ Development Environment Ready!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Activate environment (in new terminals): source .venv/bin/activate"
echo "  2. Run desktop app: python programs/mspp_app/gui_app.py"
echo "  3. Run data analysis: python programs/MSPP_data_analysis.ipynb"
echo ""
echo "See CONTRIBUTING.md for development guidelines"
echo ""
