@echo off
echo ========================================
echo QKD Simulator Web Application Setup
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed!
    echo Please download and install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Node.js found: 
node --version
echo.

REM Check if npm is installed
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm is not installed!
    pause
    exit /b 1
)

echo [OK] npm found:
npm --version
echo.

echo ========================================
echo Installing Backend Dependencies...
echo ========================================
cd backend
if not exist node_modules (
    npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Backend installation failed!
        pause
        exit /b 1
    )
    echo [OK] Backend dependencies installed!
) else (
    echo [SKIP] Backend dependencies already installed
)
echo.

echo ========================================
echo Installing Frontend Dependencies...
echo ========================================
cd ..\frontend
if not exist node_modules (
    npm install
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Frontend installation failed!
        pause
        exit /b 1
    )
    echo [OK] Frontend dependencies installed!
) else (
    echo [SKIP] Frontend dependencies already installed
)
cd ..
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo 1. Open TWO command prompts
echo.
echo 2. In Terminal 1, run:
echo    cd web\backend
echo    npm start
echo.
echo 3. In Terminal 2, run:
echo    cd web\frontend
echo    npm start
echo.
echo 4. Open browser to: http://localhost:3000
echo.
echo ========================================
pause
