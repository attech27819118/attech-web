@echo off
title ATTech Web Server (Port 9118)

REM Change to script directory
cd /d "%~dp0"

echo ========================================================
echo   Starting ATTech Server on Port 9118...
echo   Local URL: http://localhost:9118
echo ========================================================
echo.

set PORT=9118

REM Open browser
start "" "http://localhost:9118"


REM Start server
node server.js



if errorlevel 1 (
    echo.
    echo [ERROR] Server stopped unexpectedly.
    pause
)
