@echo off
title ClockTower - Backend (Django :8000)
cd /d "%~dp0backend"
echo Starting Django backend on http://localhost:8000 ...
python manage.py runserver 0.0.0.0:8000
