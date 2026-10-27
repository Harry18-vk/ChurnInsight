@echo off
title Customer Churn AI Platform
cd /d "%~dp0"
echo ========================================================
echo Starting Customer Churn AI Platform...
echo ========================================================
echo Server URL: http://127.0.0.1:5000
echo Login:      admin / admin123
echo ========================================================
start "" "http://127.0.0.1:5000"
python app\app.py
pause
