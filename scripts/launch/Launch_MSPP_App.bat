@echo off
REM MSPP Data Plotter - Desktop Launcher (Development Mode)
REM Double-click this file to launch the app in development mode with debugging enabled

setlocal enabledelayedexpansion

REM Navigate to project root
cd /d "%~dp0"

echo ===============================================================
echo Starting MSPP Data Plotter (Development Mode)
echo ===============================================================
echo.

REM Find Python executable - try venv first, then pixi, then system
set PYTHON_EXE=python.exe

if exist ".venv\Scripts\python.exe" (
    set PYTHON_EXE=.venv\Scripts\python.exe
    echo Using virtual environment: .venv
) else if exist ".pixi\envs\default\python.exe" (
    set PYTHON_EXE=.pixi\envs\default\python.exe
    echo Using pixi environment: .pixi\envs\default
) else (
    echo Using system Python
)

echo.

REM Set development environment variables
set FLASK_ENV=development
set FLASK_HOST=127.0.0.1
set FLASK_PORT=5000

REM Run the launcher
echo Launching web app on http://localhost:5000
echo.

"!PYTHON_EXE!" programs\mspp_web\launch_app.py

if errorlevel 1 (
    echo.
    echo ===============================================================
    echo ERROR: Failed to start the app. Check the message above.
    echo ===============================================================
    pause
)
