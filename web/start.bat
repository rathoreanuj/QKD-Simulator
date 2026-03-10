@echo off
echo ========================================
echo Starting QKD Simulator Web Application
echo ========================================
echo.
echo Starting Backend Server...
echo Backend will run on: http://localhost:3001
echo.
echo Starting Frontend Server...
echo Frontend will run on: http://localhost:3000
echo.
echo ========================================
echo Opening TWO terminals...
echo ========================================
echo.

REM Start backend in new window
start "QKD Backend" cmd /k "cd backend && npm start"

REM Wait 3 seconds for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "QKD Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo Servers Starting!
echo ========================================
echo.
echo Backend: http://localhost:3001
echo Frontend: http://localhost:3000
echo.
echo The browser should open automatically.
echo If not, open: http://localhost:3000
echo.
echo Close this window when done.
echo ========================================
