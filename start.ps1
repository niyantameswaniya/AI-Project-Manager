# Start AI Project Manager - Backend and Frontend
# Run this script from the project_manager folder

Write-Host "Starting AI Project Manager..." -ForegroundColor Green
Write-Host ""

# Start Backend in a new window
Write-Host "Starting Backend (port 8000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python -m uvicorn app.main:app --reload --port 8000"

# Wait for backend to start
Start-Sleep -Seconds 3

# Start Frontend in a new window
Write-Host "Starting Frontend (port 3000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "Both servers are starting in separate windows." -ForegroundColor Green
Write-Host "  Backend:  http://127.0.0.1:8000  (API docs: http://127.0.0.1:8000/docs)" -ForegroundColor Yellow
Write-Host "  Frontend: http://127.0.0.1:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Open your browser to: http://127.0.0.1:3000" -ForegroundColor Green
Write-Host "Keep both terminal windows open while using the app." -ForegroundColor Gray
