from opcua import Client
import csv
import os
from datetime import datetime
import time

# آدرس سرور OPC UA
OPC_URL = "opc.tcp://10.2.67.200:4840"
OPC_USERNAME = "KSF"
OPC_PASSWORD = "12345678"

# تابع برای ساخت نودهای اندیس‌دار
def make_indexed_nodes(base_name, count):
    """
    ساخت نودهای اندیس‌دار (از 1 شروع می‌شود)
    مثال: make_indexed_nodes("vaPower", 6) 
    نودهای vaPower[1] تا vaPower[6] را می‌سازد
    """
    nodes = {}
    for i in range(1, count + 1):
        node_name = f"{base_name}[{i}]"
        # ساخت NodeId بر اساس الگوی Sinumerik
        node_id = f"ns=2;s=/Nck/MachineAxis/{base_name}[{i}]"
        nodes[node_name] = node_id
    return nodes

# ساخت NODES با استفاده از make_indexed_nodes
NODES = {}
NODES.update(make_indexed_nodes("vaPower", 6))
NODES.update(make_indexed_nodes("vaCurr", 6))
NODES.update(make_indexed_nodes("aaTorque", 6))
NODES.update(make_indexed_nodes("aaDtbb", 6))
NODES.update(make_indexed_nodes("cmdSpeedRel", 6))

# Status nodes (only saved when value changes)
STATUS_NODES = {
    "channelNo": "ns=2;s=/Nck/LogicalSpindle/channelNo",
    "speedOvr": "ns=2;s=/Nck/LogicalSpindle/speedOvr",
    "spindleType": "ns=2;s=/Nck/LogicalSpindle/spindleType",
    "status_LogicalSpindle": "ns=2;s=/Nck/LogicalSpindle/status",
    "paramSetNo": "ns=2;s=/Nck/MachineAxis/paramSetNo",
    "status_Spindle": "ns=2;s=/Nck/Spindle/status",
    "progEvent": "ns=2;s=/Channel/State/progEvent",
    "progStatus": "ns=2;s=/Channel/State/progStatus",
    "actFeedRate": "ns=2;s=/Nck/MachineAxis/actFeedRate",
    "cmdFeedRate": "ns=2;s=/Nck/MachineAxis/cmdFeedRate",
    "cmdSpeedRel": "ns=2;s=/Nck/MachineAxis/cmdSpeedRel",
    "actParts": "ns=2;s=/Channel/State/actParts",
    "MachiningTimeRecording": "ns=2;s=/Hmi/MachiningTimeRecording",
    "toolNo": "ns=2;s=/Tool/Catalogue/toolNo",
    "actSpeed": "ns=2;s=/Channel/Spindle/actSpeed",
}

# ذخیره مقادیر قبلی STATUS_NODES برای تشخیص تغییر
previous_status_values = {}

# فاصله زمانی بین ذخیره‌سازی‌ها (ثانیه)
SAVE_INTERVAL = 60

# فاصله زمانی بین خواندن‌ها (sample rate - ثانیه)
READ_INTERVAL = 60

# مسیر فولدر ذخیره‌سازی
DATA_FOLDER = "opc data"

def read_opcua_data():
    """خواندن داده‌ها از سرور OPC UA"""
    data = {}
    try:
        client = Client(OPC_URL)
        client.set_user(OPC_USERNAME)
        client.set_password(OPC_PASSWORD)

        # اتصال بدون تنظیمات امنیتی
        # اگر نیاز به امنیت دارید، می‌توانید تنظیمات را تغییر دهید
        # client.set_security_string("None")

        client.connect()
        try:
            # خواندن NODES (همیشه ذخیره می‌شوند)
            for name, nodeid in NODES.items():
                try:
                    node = client.get_node(nodeid)
                    value = node.get_value()
                    data[name] = value
                except Exception as e:
                    data[name] = f"Error: {str(e)}"
            
            # خواندن STATUS_NODES (فقط وقتی تغییر کنند ذخیره می‌شوند)
            status_changed = False
            for name, nodeid in STATUS_NODES.items():
                try:
                    node = client.get_node(nodeid)
                    value = node.get_value()
                    # بررسی تغییر مقدار
                    if name not in previous_status_values or previous_status_values[name] != value:
                        status_changed = True
                        previous_status_values[name] = value
                    data[name] = value
                except Exception as e:
                    data[name] = f"Error: {str(e)}"
            
            data['_status_changed'] = status_changed
            
        finally:
            client.disconnect()
    except Exception as e:
        print(f"OPC UA Connection Error: {str(e)}")
        data = {"Connection": f"Error: {str(e)}"}
    return data

def save_to_csv(data_list):
    """ذخیره لیست داده‌ها در فایل CSV جدید با timestamp"""
    if not data_list:
        print("No data to save")
        return
    
    # ایجاد فولدر اگر وجود نداشته باشد
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
        print(f"Created folder: {DATA_FOLDER}")
    
    # ساخت نام فایل با timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_filename = f"opc_data_{timestamp}.csv"
    csv_file = os.path.join(DATA_FOLDER, csv_filename)
    
    # نوشتن در فایل CSV جدید
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp'] + list(NODES.keys()) + list(STATUS_NODES.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # نوشتن هدر
        writer.writeheader()
        
        # نوشتن همه ردیف‌های داده
        for data in data_list:
            # کپی کردن data برای جلوگیری از تغییر داده اصلی
            row_data = {}
            row_data['timestamp'] = data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            
            # حذف فلگ تغییر از داده
            data_copy = data.copy()
            data_copy.pop('_status_changed', None)
            
            # همیشه NODES را اضافه می‌کنیم
            for name in NODES.keys():
                row_data[name] = data_copy.get(name, '')
            
            # اضافه کردن STATUS_NODES
            for name in STATUS_NODES.keys():
                row_data[name] = data_copy.get(name, '')
            
            # نوشتن ردیف
            writer.writerow(row_data)
    
    first_timestamp = data_list[0].get('timestamp', '')
    last_timestamp = data_list[-1].get('timestamp', '')
    print(f"Data saved to {csv_file}: {len(data_list)} rows (from {first_timestamp} to {last_timestamp})")

def main():
    """تابع اصلی"""
    print("Starting OPC UA Data Logger...")
    print(f"Connecting to: {OPC_URL}")
    print(f"Monitoring {len(NODES)} indexed nodes and {len(STATUS_NODES)} status nodes")
    print(f"Sample rate: Every {READ_INTERVAL} seconds")
    print(f"Saving interval: Every {SAVE_INTERVAL} seconds")
    print(f"Each save will create a new CSV file with timestamp")
    print(f"Files will be saved in: {DATA_FOLDER}/")
    
    # بررسی مسیر فولدر
    abs_path = os.path.abspath(DATA_FOLDER)
    print(f"Absolute path: {abs_path}")
    
    # تست ایجاد فولدر
    if not os.path.exists(DATA_FOLDER):
        try:
            os.makedirs(DATA_FOLDER)
            print(f"Created folder: {DATA_FOLDER}")
        except Exception as e:
            print(f"Error creating folder: {str(e)}")
            return
    else:
        print(f"Folder exists: {DATA_FOLDER}")
    
    print("Press Ctrl+C to stop\n")
    
    # تست اولیه: بررسی اینکه آیا می‌توانیم فایل بنویسیم
    try:
        test_file = os.path.join(DATA_FOLDER, "test_write.txt")
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("Write test successful - folder is writable\n")
    except Exception as e:
        print(f"Write test failed: {str(e)}")
        print("Cannot write to folder. Please check permissions.\n")
        return
    
    file_count = 0
    try:
        while True:
            print(f"\nReading data continuously... (File #{file_count + 1})")
            
            # خواندن پیوسته با sample rate بالا تا زمان ذخیره
            start_time = time.time()
            all_data = []  # لیست همه داده‌های خوانده شده
            
            while (time.time() - start_time) < SAVE_INTERVAL:
                data = read_opcua_data()
                
                # بررسی خطای اتصال
                connection_error = data.get("Connection", "")
                if connection_error and "Error:" in str(connection_error):
                    print(f"Connection error: {connection_error}")
                    print(f"Retrying in {READ_INTERVAL} seconds...")
                else:
                    # اضافه کردن timestamp به داده
                    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # اضافه کردن داده به لیست
                    all_data.append(data)
                    elapsed = int(time.time() - start_time)
                    remaining = SAVE_INTERVAL - elapsed
                    print(f"Data read successfully. Time: {elapsed}s / {SAVE_INTERVAL}s (Remaining: {remaining}s) - Total samples: {len(all_data)}")
                
                # صبر قبل از خواندن بعدی (sample rate)
                time.sleep(READ_INTERVAL)
            
            # ذخیره همه داده‌های خوانده شده
            if all_data:
                try:
                    save_to_csv(all_data)
                    file_count += 1
                    print(f"Waiting {SAVE_INTERVAL} seconds until next save...\n")
                except Exception as save_error:
                    print(f"Error saving file: {str(save_error)}")
                    print(f"Retrying in {SAVE_INTERVAL} seconds...\n")
            else:
                print(f"No valid data to save. Retrying in {SAVE_INTERVAL} seconds...\n")
            
    except KeyboardInterrupt:
        print("\nStopping data logger...")
        print(f"Total {file_count} file(s) created during this session")

if __name__ == '__main__':
    main()
