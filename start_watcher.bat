@echo off
REM Bronze Tier AI Employee - Startup Script for Windows

echo ========================================
echo   Bronze Tier AI Employee
echo   Starting File System Watcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.13+ from python.org
    pause
    exit /b 1
)

REM Check if watchdog is installed
python -c "import watchdog" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    pip install watchdog
    echo.
)

echo Starting File System Watcher...
echo Monitoring: %CD%\Inbox
echo.
echo Press Ctrl+C to stop
echo ========================================
echo.

REM Start the watcher
python filesystem_watcher.py

pause
