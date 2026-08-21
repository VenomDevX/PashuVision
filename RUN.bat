@echo off
echo ===================================================
echo Starting PashuDrishti - Smart India Hackathon 2026
echo ===================================================
echo.
echo Cleaning up old processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000 "') do taskkill /f /pid %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":3000 "') do taskkill /f /pid %%a 2>nul

echo [1/2] Starting AI Backend (FastAPI on Port 8000)...
start "PashuDrishti Backend" cmd /k "cd backend && ..\.venv\Scripts\uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [2/2] Starting Web Frontend (Next.js on Port 3000)...
start "PashuDrishti Frontend" cmd /k "cd /d E:\PashuVision_Frontend && npm run dev"

echo.
echo Both servers are launching in separate windows!
echo Waiting 5 seconds for them to boot up...
timeout /t 5 /nobreak >nul

echo Opening PashuDrishti in Google Chrome...
start chrome http://localhost:3000
echo.
pause
