# KSF Data Collection System - Setup Guide
# راهنمای نصب و اجرای سیستم جمع‌آوری داده

## 1. نصب Python
Windows یا Linux دارای Python 3.7+ باشید.
بررسی کنید:
```powershell
python --version
```

## 2. نصب کتابخانه‌ها

### گزینه 1: استفاده از requirements.txt (توصیه شده)
```powershell
cd f:\Machines\CT\ct3
pip install -r requirements.txt
```

### گزینه 2: نصب دستی
```powershell
pip install opcua>=0.98.12
pip install daqhats>=1.4.0
pip install numpy>=1.21.0
```

## 3. اجرای سیستم

### شروع هر دو برنامه (توصیه شده)
```powershell
cd f:\Machines\CT\ct3
python start.py
```

**برای توقف:** Ctrl+C

### اجرای جداگانه

**برنامه 1: Current Logger (MCC118)**
```powershell
python "fix_current_logger (2).py"
```

**برنامه 2: OPC UA Logger (Sinumerik)**
```powershell
python "opc 828d V2.0 CSV.py"
```

## 4. خروجی‌ها

**Current Logger:**
- مسیر: `./Ziresch/current_data/`
- فرمت: `currentdata_YYYY-MM-DD_HH-MM-SS.csv`
- ستون‌ها: Time (s), Timestamp, RMS Current (A)

**OPC UA Logger:**
- مسیر: `./opc data/`
- فرمت: `opc_data_YYYYmmdd_HHMMSS.csv`
- نودها: 30 indexed nodes + 15 status nodes

## 5. پیش‌نیازهای سخت‌افزار

- **MCC118 DAC Board:** برای اندازه‌گیری جریان CT
- **OPC UA Server:** آدرس `opc.tcp://10.2.67.200:4840`
  - Username: `KSF`
  - Password: `12345678`

## 6. بررسی نصب

```powershell
# بررسی تمام کتابخانه‌ها
pip show opcua daqhats numpy

# اجرای test کوچک
python -c "import opcua, numpy, daqhats; print('All libraries imported successfully')"
```

## 7. نکات مهم

- **MCC118:** برد را باید روی کامپیوتر نصب کرده باشید
- **OPC UA:** سرور باید در دسترس باشد و اطلاعات دسترسی صحیح باشد
- **فایل‌های داده:** هر `SAVE_INTERVAL` یک فایل CSV جدید ایجاد می‌شود
- **Logs:** خروجی برنامه در console نمایش می‌یابد

## 8. رفع مشکلات

### خطای: `ModuleNotFoundError: No module named 'opcua'`
```powershell
pip install --upgrade opcua
```

### خطای: `ModuleNotFoundError: No module named 'daqhats'`
```powershell
pip install --upgrade daqhats
```

### خطای: اتصال OPC UA
- سرور IP `10.2.67.200:4840` را بررسی کنید
- username/password را تایید کنید

### خطای: MCC118 نیافت
- برد را بررسی کنید
- درایورهای USB را بروزرسانی کنید
