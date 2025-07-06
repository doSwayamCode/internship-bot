@echo off
echo ===============================================
echo    SETTING UP WINDOWS TASK SCHEDULER
echo ===============================================
echo.
echo This will create a scheduled task to run your internship bot automatically every 5 hours.
echo.
pause

REM Create the scheduled task
schtasks /create /tn "InternshipBot" /tr "cd /d \"%~dp0\" && python smart_scheduler.py" /sc hourly /mo 5 /st 09:00 /f

if %errorlevel% == 0 (
    echo.
    echo ✅ SUCCESS! Scheduled task created.
    echo.
    echo 📅 Your bot will now run automatically:
    echo    - Every 5 hours starting at 9:00 AM
    echo    - Runs in background without terminal windows
    echo.
    echo 🔧 To manage the task:
    echo    - Open "Task Scheduler" from Start menu
    echo    - Look for "InternshipBot" task
    echo.
    echo 🛑 To stop/disable:
    echo    - Run: schtasks /delete /tn "InternshipBot" /f
    echo.
) else (
    echo.
    echo ❌ ERROR: Could not create scheduled task.
    echo    Please run this script as Administrator.
    echo.
)

pause
