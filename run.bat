@echo off
cd /d "%~dp0"
title AI Project Manager

echo ============================================
echo   AI Project Manager
echo ============================================
echo.

REM Build frontend only if dist missing (optional - backend will still run)
if not exist "frontend\dist\index.html" (
    echo [Step 1] Building frontend (first time)...
    cd frontend
    call npm run build 2>nul
    if errorlevel 1 (
        echo   Build failed - run build-frontend.bat manually later.
        echo   Backend will start anyway. You can use http://127.0.0.1:8000/docs
        echo.
    ) else (
        echo   Build done.
    )
    cd ..
) else (
    echo [Step 1] Frontend already built.
)
echo.

echo [Step 2] Starting server...
echo.
echo   OPEN IN BROWSER:  http://127.0.0.1:8000
echo   (Keep this window open.)
echo ============================================
echo.

cd backend
python -m uvicorn app.main:app --port 8000

if errorlevel 1 (
    echo.
    echo Error: Backend did not start.
    echo - Install Python if needed: https://www.python.org/downloads/
    echo - In backend folder run: pip install -r requirements.txt
    echo.
)
pause
