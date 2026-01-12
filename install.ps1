# KSF Data Collection System - Installation Script for Windows
# اسکریپت نصب برای Windows

Write-Host "==========================================" -ForegroundColor Green
Write-Host "KSF Data Collection System - Setup" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""

# بررسی Python
Write-Host "[1/4] بررسی Python..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python پیدا نشد. لطفا Python را نصب کنید." -ForegroundColor Red
    exit 1
}
Write-Host ""

# بروز رسانی pip
Write-Host "[2/4] بروز رسانی pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip setuptools wheel | Out-Null
Write-Host "✓ pip بروز رسانی شد" -ForegroundColor Green
Write-Host ""

# نصب کتابخانه‌ها
Write-Host "[3/4] نصب کتابخانه‌ها..." -ForegroundColor Cyan
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Host "✓ تمام کتابخانه‌ها نصب شدند" -ForegroundColor Green
} else {
    Write-Host "ERROR: requirements.txt پیدا نشد" -ForegroundColor Red
    exit 1
}
Write-Host ""

# بررسی نصب
Write-Host "[4/4] بررسی نصب..." -ForegroundColor Cyan
try {
    python -c "import opcua, numpy; print('All modules imported successfully')" 2>&1 | Out-Null
    Write-Host "✓ تمام کتابخانه‌ها موفق نصب شدند" -ForegroundColor Green
} catch {
    Write-Host "WARNING: ممکن است برخی کتابخانه‌ها نصب نشده‌اند" -ForegroundColor Yellow
}
Write-Host ""

# خلاصه
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✓ نصب کامل شد!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "برای اجرای برنامه:" -ForegroundColor Yellow
Write-Host "  cd f:\Machines\CT\ct3" -ForegroundColor White
Write-Host "  python start.py" -ForegroundColor White
Write-Host ""
