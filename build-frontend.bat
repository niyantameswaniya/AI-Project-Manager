@echo off
cd /d "%~dp0\frontend"
title Build Frontend

echo Installing and building frontend...
echo.
call npm install
if errorlevel 1 (
    echo npm install failed. Install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo.
call npm run build
if errorlevel 1 (
    echo Build failed.
    pause
    exit /b 1
)
echo.
echo Done. Now run run.bat to start the app.
pause
