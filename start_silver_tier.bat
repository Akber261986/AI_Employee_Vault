@echo off
REM Silver Tier AI Employee - Master Orchestrator Startup (Windows)

echo ========================================
echo   Silver Tier AI Employee
echo   Starting Master Orchestrator
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

REM Check dependencies
python -c "import watchdog, google.auth, playwright" >nul 2>&1
if errorlevel 1 (
    echo Installing Silver Tier dependencies...
    pip install -e .
    playwright install chromium
    echo.
)

echo Starting Orchestrator...
echo.
echo This will start:
echo - Gmail Watcher
echo - File System Watcher
echo.
echo Press Ctrl+C to stop all watchers
echo ========================================
echo.

python orchestrator.py

pause
