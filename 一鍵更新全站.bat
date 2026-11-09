@echo off
title ATTech Site Builder
cd /d "%~dp0"

node -v >nul 2>&1
if errorlevel 1 (
    echo.
    echo [ERROR] Node.js is not found or not installed!
    echo.
    pause
    exit /b 1
)

node scripts/build_all.js
if errorlevel 1 (
    echo.
    echo [Build Failed] Please check the error message above.
    echo.
    pause
    exit /b 1
)

echo.
pause
exit /b 0
