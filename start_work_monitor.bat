@echo off
REM Quick start script for scheduled ClickUp monitoring
REM Runs 20 min on / 20 min off from 9:43 AM - 5:00 PM CST

echo ==========================================
echo   ClickUp Monitor - TEST SCHEDULE (1/16/25)
echo ==========================================
echo.
echo Schedule: 9:44 AM - 5:00 PM CST
echo Pattern:  15 min ON / 15 min OFF
echo.
echo Starting monitor...
echo Press Ctrl+C to stop anytime
echo.
echo ==========================================
echo.

python src\clickup_monitor_scheduled.py

echo.
echo ==========================================
echo   Monitoring stopped
echo ==========================================
pause
