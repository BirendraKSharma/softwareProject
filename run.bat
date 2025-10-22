@echo off
echo ========================================
echo   Hospital Management System
echo   Starting Application...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo   Application is starting!
echo   Open your browser and visit:
echo   http://localhost:5000
echo.
echo   Admin Login:
echo   Email: admin@hms.com
echo   Password: admin123
echo ========================================
echo.

REM Run the application
python main.py

pause
