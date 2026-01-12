@echo off
REM run.bat - Quick launcher for KSF Data Collection System
REM فقط run.bat رو کلیک کن و همه چیز خودکار فعال می‌شود

setlocal enabledelayedexpansion

cd /d "%~dp0"

REM بررسی virtual environment
if not exist "venv" (
    echo Virtual environment یافت نشد. در حال ایجاد...
    python -m venv venv
)

REM فعال کردن virtual environment
echo فعال کردن virtual environment...
call venv\Scripts\activate.bat

REM بررسی کتابخانه‌ها
python -c "import opcua" >nul 2>&1
if errorlevel 1 (
    echo کتابخانه‌های مورد نیاز نصب نشده‌اند. در حال نصب...
    pip install -r requirements.txt >nul
)

echo.
echo ========================================
echo KSF Data Collection System
echo ========================================
echo.
python start.py

pause
