@echo off
echo ============================================
echo    QKD Simulator Launcher
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    echo.
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if required packages are installed
echo Checking for required packages...
python -c "import qiskit" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Installing required packages...
    echo This may take a few minutes...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install packages
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
) else (
    echo All packages installed!
)

echo.
echo ============================================
echo    Launching QKD Simulator...
echo ============================================
echo.

python qkd_gui.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Program exited with error
    pause
)
