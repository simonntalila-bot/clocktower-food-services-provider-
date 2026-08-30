@echo off
title ClockTower - Start All
echo ============================================
echo  ClockTower - Starting all services
echo  - Backend (Django)  : http://localhost:8000
echo  - Storefront (Vite) : http://localhost:5173
echo ============================================
echo.

start "ClockTower - Backend (Django :8000)" cmd /c call "%~dp0start-backend.bat"
start "ClockTower - Storefront (Vite :5173)" cmd /c call "%~dp0start-storefront.bat"

echo Both services started in separate windows.
echo Close them individually when done.
pause
