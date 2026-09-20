@echo off
cd /d "%~dp0\backend"
title Backend - Port 8000

echo ============================================
echo   Backend only - http://127.0.0.1:8000
echo ============================================
echo.

REM Free port 8000 if already in use (e.g. previous run)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
    timeout /t 1 /nobreak >nul
)
echo.

echo Open in browser:  http://127.0.0.1:8000
echo API docs:         http://127.0.0.1:8000/docs
echo.
echo (Full app: run build-frontend.bat then run.bat)
echo ============================================
echo.

python -m uvicorn app.main:app --port 8000

if errorlevel 1 (
    echo.
    echo If "port in use" error: close other backend window or run kill-port-8000.bat
    echo Other error: try  pip install -r requirements.txt
)
pause
