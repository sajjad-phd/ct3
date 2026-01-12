#!/usr/bin/env python3
"""
start.py - Launcher for multiple data collection processes
اجرای خودکار دو برنامه‌ی جمع‌آوری داده
"""

import subprocess
import sys
import os
import signal
import time
from datetime import datetime

# مسیر فایل‌های اسکریپت
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT_1 = os.path.join(CURRENT_DIR, "current_logger.py")
SCRIPT_2 = os.path.join(CURRENT_DIR, "opc_logger.py")

# لیست برای نگهداری از processes
processes = []

def print_header():
    """چاپ هدر شروع برنامه"""
    print("\n" + "="*70)
    print(" "*15 + "KSF Data Collection System - Start")
    print("="*70)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Working Directory: {CURRENT_DIR}")
    print("="*70 + "\n")

def start_process(script_path, name):
    """شروع یک process جدید"""
    if not os.path.exists(script_path):
        print(f"ERROR: Script not found: {script_path}")
        return None
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting: {name}...")
    try:
        # اجرای اسکریپت با Python
        # shell=False برای امنیت بیشتر
        process = subprocess.Popen(
            [sys.executable, script_path],
            cwd=CURRENT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1  # Line buffered
        )
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {name} started (PID: {process.pid})")
        return process
    except Exception as e:
        print(f"ERROR starting {name}: {str(e)}")
        return None

def monitor_processes():
    """نگاه‌داشتن بر روی processes و نمایش خروجی آن‌ها"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] All processes started. Monitoring...\n")
    print("Press Ctrl+C to stop all processes\n")
    print("-"*70)
    
    try:
        while True:
            # بررسی اینکه آیا processes هنوز زنده‌اند
            for i, (process, name) in enumerate(zip(processes, ["Current Logger", "OPC UA Logger"])):
                if process is not None:
                    poll_result = process.poll()
                    if poll_result is not None:
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] WARNING: {name} has stopped (exit code: {poll_result})")
                        print("Attempting to restart...\n")
                        processes[i] = start_process(
                            [SCRIPT_1, SCRIPT_2][i],
                            name
                        )
            
            # خواندن خروجی از processes
            for process, name in zip(processes, ["Current Logger", "OPC UA Logger"]):
                if process is not None and process.poll() is None:
                    try:
                        # تلاش برای خواندن خروجی بدون مسدود کردن
                        # این روش ساده‌تر است
                        pass
                    except:
                        pass
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n\n[{datetime.now().strftime('%H:%M:%S')}] Ctrl+C detected. Stopping all processes...\n")
        stop_all_processes()

def stop_all_processes():
    """متوقف کردن همه‌ی processes"""
    for process, name in zip(processes, ["Current Logger", "OPC UA Logger"]):
        if process is not None and process.poll() is None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Stopping {name} (PID: {process.pid})...")
            try:
                # ارسال SIGTERM برای خروج نرم
                process.terminate()
                # انتظار 5 ثانیه برای خروج
                try:
                    process.wait(timeout=5)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {name} stopped gracefully")
                except subprocess.TimeoutExpired:
                    # اگر نتوانست خروج کند، از SIGKILL استفاده کن (فقط در Unix)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {name} did not stop, forcing kill...")
                    process.kill()
                    process.wait()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {name} killed")
            except Exception as e:
                print(f"ERROR stopping {name}: {str(e)}")

def signal_handler(sig, frame):
    """مدیریت سیگنال‌های interrupt"""
    print(f"\n\n[{datetime.now().strftime('%H:%M:%S')}] Signal {sig} received. Shutting down...\n")
    stop_all_processes()
    sys.exit(0)

def main():
    """تابع اصلی"""
    print_header()
    
    # ثبت signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)
    
    # اجرای اسکریپت‌ها
    print("Starting data collection processes...\n")
    
    p1 = start_process(SCRIPT_1, "Current Logger (MCC118 RMS)")
    time.sleep(1)  # تاخیر کوچک بین شروع دو process
    p2 = start_process(SCRIPT_2, "OPC UA Logger (Sinumerik)")
    
    processes.append(p1)
    processes.append(p2)
    
    # بررسی اینکه آیا هر دو process شروع شدند
    if p1 is None or p2 is None:
        print("\nERROR: Failed to start one or more processes")
        stop_all_processes()
        sys.exit(1)
    
    print()
    
    # مراقبت از processes
    monitor_processes()
    
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] All processes have been stopped")
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
