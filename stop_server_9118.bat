@echo off
title Stop ATTech Web Server (Port 9118)
echo ========================================================
echo   Stopping ATTech Server on Port 9118...
echo ========================================================

powershell -NoProfile -Command "try { $conn = Get-NetTCPConnection -LocalPort 9118 -State Listen -ErrorAction Stop; Stop-Process -Id $conn.OwningProcess -Force; Write-Host '[OK] ATTech Server (PID '$conn.OwningProcess') stopped successfully.' -ForegroundColor Green } catch { Write-Host '[INFO] No server was running on Port 9118.' -ForegroundColor Yellow }"

echo.
timeout /t 3

