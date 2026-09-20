@echo off
cd /d "%~dp0\frontend"
title Frontend - AI Project Manager (Port 3000)

echo Starting Frontend on http://127.0.0.1:3000
echo.
echo If you see "Local: http://localhost:3000/" below, frontend is OK.
echo Then open in your browser: http://127.0.0.1:3000
echo Keep this window open.
echo.
echo ----------------------------------------

npm run dev

echo.
echo Frontend stopped.
pause
