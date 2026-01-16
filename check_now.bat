@echo off
echo ==========================================
echo   ClickUp Task Checker
echo ==========================================
echo.
echo Checking your ClickUp workspace...
echo.

python src\clickup_monitor.py --once

echo.
echo ==========================================
echo   Check complete!
echo ==========================================
pause
