@echo off
echo ===============================================
echo    SMART INTERNSHIP BOT - EMAIL ONLY
echo ===============================================
echo Starting intelligent internship automation...
echo.
echo Features:
echo - Searches until NEW internships are found
echo - Email notifications only (no WhatsApp)
echo - Multiple sources: Internshala, Naukri, Glassdoor, Unstop
echo - No duplicate notifications
echo - Smart filtering for tech and relevant roles
echo.
echo Press Ctrl+C to stop anytime
echo ===============================================
echo.

cd /d "%~dp0"
python smart_scheduler.py

pause
