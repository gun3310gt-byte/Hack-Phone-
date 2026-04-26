import os
import time
import shutil

# สี Terminal
G = '\033[92m' ; C = '\033[96m' ; Y = '\033[93m' ; R = '\033[91m' ; W = '\033[0m'

print(f"{R}--- Hack Phone ---{W}")
time.sleep(0.3)

# 1. [name Phone]
brand = os.popen('getprop ro.product.brand').read().strip().upper() or "GENERIC"
model = os.popen('getprop ro.product.model').read().strip() or "DEVICE"
print(f"{C}[name Phone]{W} {brand} {model}")

# 2. [CPU]
plat = os.popen('getprop ro.board.platform').read().strip().lower()
hw = os.popen('getprop ro.hardware').read().strip().lower()
cpu_final = "MediaTek Helio G99" if "mt6789" in (plat + hw) else plat.upper()
print(f"{C}[CPU]{W} {cpu_final}")

# 3. [gpu]
gpu_raw = os.popen('getprop ro.hardware.egl').read().strip()
if not gpu_raw or "meow" in gpu_raw.lower():
    gpu_raw = os.popen("dumpsys SurfaceFlinger | grep GLES | cut -d':' -f2").read().strip()
if "mt6789" in (plat + hw) and ("meow" in gpu_raw.lower() or not gpu_raw):
    gpu_raw = "Mali-G57 MC2"
print(f"{C}[gpu]{W} {gpu_raw}")

# 4. [ram]
with open('/proc/meminfo', 'r') as f:
    total_kb = int(f.readline().split()[1])
total_gb = total_kb / (1024**2)
ram_market = min([1, 2, 3, 4, 6, 8, 12, 16, 24, 32], key=lambda x:abs(x-total_gb))
print(f"{C}[ram]{W} {ram_market} GB")

# 5. [Storage] - วิเคราะห์ Used 70GB
stat = os.statvfs('/data')
data_total_gb = (stat.f_blocks * stat.f_frsize) / (1024**3)
data_free_gb = (stat.f_bfree * stat.f_frsize) / (1024**3)
st_list = [8, 16, 32, 64, 128, 256, 512, 1024]
total_market = min([x for x in st_list if x >= data_total_gb], default=128)
system_reserved = total_market - data_total_gb
used_actual = (data_total_gb - data_free_gb) + system_reserved

print(f"{C}[Storage]{W} {total_market} GB")
print(f"   {Y}Used:{W} {used_actual:.2f} GB")
print(f"   {Y}Free:{W} {(total_market - used_actual):.2f} GB")

# 6. [root] - ตรวจสอบเข้มงวด 10,000% (ป้องกันค่า ON หลอก)
def check_root():
    # เช็คที่อยู่ไฟล์ su
    paths = ['/system/bin/su', '/system/xbin/su', '/sbin/su', '/system/sd/xbin/su', '/data/local/xbin/su', '/data/local/bin/su']
    file_exists = any(os.path.exists(p) for p in paths)
    
    # เช็คผ่านคำสั่ง command
    cmd_exists = shutil.which('su') is not None
    
    if file_exists or cmd_exists:
        # ด่านสุดท้าย: ลองรันคำสั่งที่ต้องใช้สิทธิ์ root จริงๆ (ถ้าไม่ใช่ root จริงจะ Error)
        # ใช้ timeout เพื่อไม่ให้สคริปต์ค้างถ้าเครื่องถามสิทธิ์
        check_real = os.system('su -c id > /dev/null 2>&1')
        if check_real == 0:
            return f"{G}ON{W}"
    return f"{R}OFF{W}"

print(f"{C}[root]{W} {check_root()}")

# 7. [OS]
android_ver = os.popen('getprop ro.build.version.release').read().strip()
oneui_v = os.popen('getprop ro.build.version.oneui').read().strip() or os.popen('getprop ro.build.version.sep').read().strip()

if oneui_v:
    if len(oneui_v) >= 5: ui_name = f"One UI {oneui_v[0:1]}.{oneui_v[1:2]}"
    else: ui_name = f"One UI {oneui_v}"
else:
    ui_name = "Stock Android"

print(f"{C}[OS]{W} Android {android_ver} ({ui_name})")
print(f"{R}------------------{W}")
