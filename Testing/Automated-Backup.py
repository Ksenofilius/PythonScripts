import shutil
import time

def backup_directory(source, destination):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    backup_file = f"{destination}/backup_{timestamp}.tar.gz"
    shutil.make_archive(backup_file.replace(".tar.gz", ""), 'gztar', source)
    print(f"Backup completed: {backup_file}")

backup_directory("/path/to/important/data", "/path/to/backup/location")
