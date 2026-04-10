@echo off
REM MSPP Data Plotter - Desktop Window Launcher
REM Double-click this file to launch the app as a native desktop window

setlocal enabledelayedexpansion

REM Navigate to project root (from scripts/launch directory, go up 2 levels)
cd /d "%~dp0..\.." 

echo ===============================================================
echo Starting MSPP Desktop App (pywebview)
echo ===============================================================
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

REM Check if system Python exists
for /f "tokens=*" %%i in ('python --version 2^>nul') do (
    set PYTHON_VERSION=%%i
)

if defined PYTHON_VERSION (
    set "PYTHON_EXE=python.exe"
    set "PYTHON_SOURCE=system Python"
    goto PythonFound
)

echo ERROR: Python not found! Please run the setup script.
pause
exit /b 1

:PythonFound
echo Using Python from: !PYTHON_SOURCE!

REM Set production variables
set FLASK_ENV=production
set FLASK_HOST=127.0.0.1
set FLASK_PORT=8051

"!PYTHON_EXE!" scripts\launch\desktop_app.py

if errorlevel 1 (
    echo.
    echo ===============================================================
    echo ERROR: App exited with an error. 
    echo ===============================================================
    pause
)
