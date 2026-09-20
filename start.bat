@echo off
cd /d "%~dp0"

echo ============================================
echo   AI Project Manager
echo ============================================
echo.
echo Opening Backend and Frontend in two new windows...
echo.

start "Backend (8000)" cmd /k "call ""%~dp0start-backend.bat"""
timeout /t 4 /nobreak >nul
start "Frontend (3000)" cmd /k "call ""%~dp0start-frontend.bat"""

echo.
echo Two windows should have opened.
echo 1. Wait until Backend shows: Uvicorn running on http://127.0.0.1:8000
echo 2. Wait until Frontend shows: Local: http://localhost:3000/
echo 3. Open in browser: http://127.0.0.1:3000
echo.
pause
