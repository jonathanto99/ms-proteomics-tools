#!/usr/bin/env pwsh
# Quick setup script for new developers
# Run: .\scripts\setup_dev.ps1

Write-Host "🔬 BYU MS Core Lab - Development Environment Setup" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "📋 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.1[0-4]") {
    Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
} else {
    Write-Host "⚠️  Python 3.10+ recommended. Found: $pythonVersion" -ForegroundColor Yellow
    Write-Host "   Continue anyway? (Ctrl+C to cancel, Enter to continue)" -ForegroundColor Yellow
    Read-Host
}

# Create virtual environment
Write-Host ""
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "⚠️  Virtual environment already exists. Skipping..." -ForegroundColor Yellow
} else {
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install Python dependencies (including dev tools)
Write-Host ""
Write-Host "📥 Installing Python dependencies..." -ForegroundColor Yellow
pip install -e ".[dev]" --quiet
Write-Host "✅ Python dependencies installed" -ForegroundColor Green

# Check if Node.js is installed
Write-Host ""
Write-Host "📋 Checking Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($nodeVersion -match "v\d+\.\d+\.\d+") {
    Write-Host "✅ Node.js $nodeVersion detected" -ForegroundColor Green
    
    # Install frontend dependencies
    Write-Host ""
    Write-Host "📥 Installing frontend dependencies..." -ForegroundColor Yellow
    Push-Location programs\mspp_web\frontend
    npm install --silent
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
    Pop-Location
} else {
    Write-Host "⚠️  Node.js not found. Web app frontend will not be available." -ForegroundColor Yellow
    Write-Host "   Install from: https://nodejs.org/" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "✨ Development Environment Ready!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Activate environment: .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. Run data analysis: python programs\python\MSPP_data_analysis.ipynb" -ForegroundColor White
Write-Host "  3. Run web app: python programs\mspp_web\backend\app.py" -ForegroundColor White
Write-Host "     (in another terminal: cd programs\mspp_web\frontend && npm run dev)" -ForegroundColor White
Write-Host ""
Write-Host "See CONTRIBUTING.md for development guidelines" -ForegroundColor Cyan
Write-Host ""
