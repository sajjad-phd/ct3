#!/bin/bash
# KSF Data Collection System - Installation Script for Linux/Raspberry Pi
# اسکریپت نصب برای Raspberry Pi و سیستم‌های Linux

set -e

echo "=========================================="
echo "KSF Data Collection System - Setup"
echo "=========================================="
echo ""

# بررسی Python
echo "[1/5] بررسی Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 پیدا نشد. لطفا Python 3 را نصب کنید."
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✓ Python found: $PYTHON_VERSION"
echo ""

# ایجاد virtual environment
echo "[2/5] ایجاد virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment ایجاد شد"
else
    echo "✓ Virtual environment قبلا وجود داشت"
fi
echo ""

# فعال کردن virtual environment
echo "[3/5] فعال کردن virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment فعال شد"
echo ""

# بروز رسانی pip
echo "[4/5] بروز رسانی pip..."
pip install --upgrade pip setuptools wheel
echo "✓ pip بروز رسانی شد"
echo ""

# نصب کتابخانه‌ها
echo "[5/5] نصب کتابخانه‌ها..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✓ تمام کتابخانه‌ها نصب شدند"
else
    echo "ERROR: requirements.txt پیدا نشد"
    exit 1
fi
echo ""

# بررسی نصب
echo "=========================================="
echo "✓ نصب کامل شد!"
echo "=========================================="
echo ""
echo "برای اجرای برنامه:"
echo "  source venv/bin/activate"
echo "  python start.py"
echo ""
echo "برای خروج از virtual environment:"
echo "  deactivate"
echo ""
