#!/bin/bash
# run.sh - Quick launcher for KSF Data Collection System
# فقط run.sh رو اجرا کن و همه چیز خودکار فعال می‌شود

set -e

# دریافت مسیر مطلق این اسکریپت
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Working Directory: $PWD"

# بررسی virtual environment
if [ ! -d "venv" ]; then
    echo "Virtual environment یافت نشد. در حال ایجاد..."
    python3 -m venv venv
fi

# فعال کردن virtual environment
echo "فعال کردن virtual environment..."
source venv/bin/activate

# بررسی کتابخانه‌ها
if ! python -c "import opcua" 2>/dev/null; then
    echo "کتابخانه‌های مورد نیاز نصب نشده‌اند. در حال نصب..."
    pip install -r requirements.txt >/dev/null
fi

# تایید مسیر کاری
echo "Current working directory: $(pwd)"
echo ""
echo "========================================"
echo "KSF Data Collection System"
echo "========================================"
echo ""
python start.py
