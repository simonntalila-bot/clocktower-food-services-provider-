@echo off
title ClockTower - Storefront Dev (Vite :5173)
cd /d "%~dp0clocktower-vue"
echo Starting Vite dev server on http://localhost:5173 ...
call npx vite --port 5173 --strictPort --host
