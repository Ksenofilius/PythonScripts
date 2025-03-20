import shutil

def check_disk_usage(path="/"):
    total, used, free = shutil.disk_usage(path)
    usage_percentage = (used / total) * 100
    if usage_percentage > 80:
        print(f"Warning! Disk usage is {usage_percentage:.2f}%")
    else:
        print(f"Disk usage is {usage_percentage:.2f}%")

check_disk_usage()
