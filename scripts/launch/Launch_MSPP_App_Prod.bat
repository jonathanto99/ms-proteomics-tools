@echo off
REM MSPP Data Plotter - Desktop Launcher (Production Mode)
REM Double-click this file to launch the app in production mode (optimized performance)

setlocal enabledelayedexpansion

REM Navigate to project root (from scripts/launch directory, go up 2 levels)
cd /d "%~dp0..\.." 

REM Verify we're in the correct directory
if not exist "scripts\launch\launcher.py" (
    echo.
    echo ERROR: Could not find launcher.py!
    echo.
    echo Expected: %CD%\scripts\launch\launcher.py
    echo.
    echo This usually means the script was moved or the path is incorrect.
    echo.
    pause
    exit /b 1
)

echo ===============================================================
echo Starting MSPP Data Plotter (Production Mode)
echo ===============================================================
echo.
echo Project Root: %CD%
echo.

REM Find Python executable - try venv first, then pixi, then system
set PYTHON_EXE=python.exe
set PYTHON_SOURCE=

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
    set "PYTHON_SOURCE=virtual environment (.venv)"
    goto PythonFound
)

if exist ".pixi\envs\default\python.exe" (
    set "PYTHON_EXE=.pixi\envs\default\python.exe"
    set "PYTHON_SOURCE=pixi environment (.pixi\envs\default)"
    goto PythonFound
)

REM Check if system Python exists and works
for /f "tokens=*" %%i in ('python --version 2^>nul') do (
    set PYTHON_VERSION=%%i
)

if defined PYTHON_VERSION (
    set "PYTHON_EXE=python.exe"
    set "PYTHON_SOURCE=system Python"
    goto PythonFound
)

REM Python not found
echo.
echo ERROR: Python not found or not properly installed!
echo.
echo To fix this, run one of these setup commands:
echo.
echo Option 1 - Automated Setup (Recommended):
echo   .\scripts\setup_dev.ps1
echo.
echo Option 2 - Python Setup Tool:
echo   python scripts\setup_dev.py
echo.
echo Option 3 - Bash Setup (Git Bash or WSL):
echo   bash scripts\setup_dev.sh
echo.
echo If you don't have Python installed:
echo   Download from: https://www.python.org/downloads/
echo.
pause
exit /b 1

:PythonFound
echo Using Python from: !PYTHON_SOURCE!
echo.

REM Verify Python works by checking version
"!PYTHON_EXE!" --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python found but not working properly
    echo Path: !PYTHON_EXE!
    echo.
    echo Try reinstalling Python or running the setup script:
    echo   .\scripts\setup_dev.ps1
    echo.
    pause
    exit /b 1
)

echo.

REM Set production environment variables (no debugging, optimized)
set FLASK_ENV=production
set FLASK_HOST=127.0.0.1
set FLASK_PORT=5000

echo Launching web app on http://localhost:5000 (production mode)
echo.

"!PYTHON_EXE!" scripts\launch\launcher.py --prod

if errorlevel 1 (
    echo.
    echo ===============================================================
    echo ERROR: Failed to start the app. Check the message above.
    echo ===============================================================
    pause
)
