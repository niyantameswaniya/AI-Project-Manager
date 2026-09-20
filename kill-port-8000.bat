@echo off
echo Freeing port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process PID %%a
    taskkill /PID %%a /F 2>nul
)
echo Done. Now run run-backend-only.bat
pause
