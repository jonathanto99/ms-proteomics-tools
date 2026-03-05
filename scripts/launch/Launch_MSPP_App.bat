@echo off
REM MSPP Data Plotter - Desktop Launcher (Development Mode)
REM Double-click this file to launch the app in development mode with debugging enabled

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
echo Starting MSPP Data Plotter (Development Mode)
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

REM Set development environment variables
set FLASK_ENV=development
set FLASK_HOST=127.0.0.1
set FLASK_PORT=5000

REM Run the launcher
echo Attempting to launch: %CD%\scripts\launch\launcher.py
echo.

"!PYTHON_EXE!" "%CD%\scripts\launch\launcher.py"

if errorlevel 1 (
    echo.
    echo ===============================================================
    echo ERROR: Failed to start the app. Check the message above.
    echo ===============================================================
    echo.
    echo Debug Info:
    echo   Python: !PYTHON_EXE!
    echo   Script: %CD%\scripts\launch\launcher.py
    echo   FLASK_ENV: %FLASK_ENV%
    echo   FLASK_PORT: %FLASK_PORT%
    echo.
    pause
)
