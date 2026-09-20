@echo off
cd /d "%~dp0\backend"
title Backend - AI Project Manager (Port 8000)

echo Starting Backend on http://127.0.0.1:8000
echo.
echo If you see "Uvicorn running on..." below, backend is OK.
echo Keep this window open. Open browser to http://127.0.0.1:3000 after starting frontend.
echo.
echo ----------------------------------------

python -m uvicorn app.main:app --reload --port 8000

echo.
echo Backend stopped.
pause
