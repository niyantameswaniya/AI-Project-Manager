@echo off
cd /d "%~dp0"
echo ============================================
echo   AI Project Manager - Setup Check
echo ============================================
echo.

echo Checking Python...
python --version 2>nul
if errorlevel 1 (
    echo   [FAIL] Python not found. Install Python 3.9+ and add to PATH.
    goto :problems
) else (
    echo   [OK] Python found.
)
echo.

echo Checking Node.js...
node --version 2>nul
if errorlevel 1 (
    echo   [FAIL] Node.js not found. Install Node.js and add to PATH.
    goto :problems
) else (
    echo   [OK] Node.js found.
)
echo.

echo Checking backend dependencies...
cd backend
python -c "import fastapi, uvicorn" 2>nul
if errorlevel 1 (
    echo   [WARN] Backend packages missing. Run: pip install -r requirements.txt
    set NEED_PIP=1
) else (
    echo   [OK] Backend packages installed.
)
cd ..
echo.

echo Checking frontend dependencies...
if not exist "frontend\node_modules" (
    echo   [WARN] Frontend node_modules missing. Run in frontend folder: npm install
    set NEED_NPM=1
) else (
    echo   [OK] Frontend node_modules found.
)
echo.

if defined NEED_PIP (
    echo Install backend deps:  cd backend ^&^& pip install -r requirements.txt
    echo.
)
if defined NEED_NPM (
    echo Install frontend deps: cd frontend ^&^& npm install
    echo.
)

echo ============================================
echo   Next: Run start-backend.bat then start-frontend.bat
echo   Or run start.bat to open both.
echo ============================================
goto :end

:problems
echo.
echo Fix the issues above, then run this check again.
echo.

:end
pause
