@echo off
echo ===============================================
echo    INTERNSHIP BOT - BACKGROUND SERVICE
echo ===============================================
echo Starting automated background service...
echo.
echo Features:
echo - Runs automatically every 5 hours
echo - No need to keep terminal open
echo - Logs all activity to background_service.log
echo - Smart email frequency control
echo.
echo Press Ctrl+C to stop the service
echo ===============================================
echo.

cd /d "%~dp0"
python background_service.py

pause
