# KSF Data Collection System

سریع‌ترین راه برای شروع:

## Raspberry Pi

```bash
cd ~/ct3
chmod +x run.sh
./run.sh
```

یا فقط:
```bash
cd ct3 && ./run.sh
```

## Windows

دوبل‌کلیک کنید روی:
```
run.bat
```

یا در PowerShell:
```powershell
cd ct3
.\run.bat
```

---

## هنوز مشکل داری؟

اگر اول‌بار است، ابتدا نصب کامل انجام بده:

### Raspberry Pi (اول‌بار)
```bash
cd ~/ct3
chmod +x install.sh
./install.sh
./run.sh
```

### Windows (اول‌بار)
```powershell
cd ct3
powershell -ExecutionPolicy Bypass -File .\install.ps1
.\run.bat
```

---

## نقاط مهم

- `run.sh` / `run.bat` هر بار virtual environment را فعال می‌کنند
- کتابخانه‌ها خودکار بررسی و نصب می‌شوند
- هر دو برنامه (OPC Logger و Current Logger) خودکار شروع می‌شوند

---

## داده‌ها کجا ذخیره می‌شوند؟

- **OPC UA**: `./opc data/`
- **Current Logger**: `./Ziresch/current_data/`

---

## توقف برنامه

فقط **Ctrl+C** را فشار دهید
