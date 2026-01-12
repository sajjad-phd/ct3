# KSF Data Collection System - Installation Instructions
# راهنمای نصب برای تمام سیستم‌ها

## Windows Setup

### روش 1: استفاده از PowerShell Script (ساده‌ترین)
```powershell
cd f:\Machines\CT\ct3
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

### روش 2: دستی
```powershell
cd f:\Machines\CT\ct3
pip install -r requirements.txt
python start.py
```

---

## Raspberry Pi / Linux Setup

### روش 1: استفاده از Bash Script (ساده‌ترین)
```bash
cd ~/ct3
chmod +x install.sh
./install.sh
```

سپس برای اجرا:
```bash
source venv/bin/activate
python start.py
```

### روش 2: دستی
```bash
cd ~/ct3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python start.py
```

---

## بررسی نصب

### Windows
```powershell
pip show opcua daqhats numpy
```

### Linux/Raspberry Pi
```bash
source venv/bin/activate
pip show opcua daqhats numpy
```

---

## خروج از Virtual Environment (فقط Linux)

```bash
deactivate
```

---

## اگر خطا داشتید

### Windows - خطای Execution Policy
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
```

### Linux - خطای Permission
```bash
chmod +x install.sh
```

### خطای ModuleNotFoundError
- مطمئن شوید virtual environment فعال است
- دوباره `pip install -r requirements.txt` اجرا کنید

---

## نکات مهم

- **Windows:** اگر PowerShell Script کار نکرد، دستی نصب کنید
- **Raspberry Pi:** حتما virtual environment استفاده کنید
- **سرور:** اطمینان حاصل کنید OPC UA سرور در دسترس است
- **MCC118:** درایورها باید نصب باشند

