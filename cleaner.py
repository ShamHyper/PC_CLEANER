import os
import shutil
import subprocess

### CLEANER 1.x ###

user_profile = os.getenv('USERPROFILE')
system_root = os.getenv('SystemRoot') 

folders_to_clear = [
    os.path.join(system_root, 'Temp'),
    os.path.join(user_profile, 'AppData', 'Local', 'Temp'),
    os.path.join(system_root, 'SoftwareDistribution', 'Download'),
    os.path.join(system_root, 'Prefetch'),
    os.path.join(user_profile, 'AppData', 'Local', 'NVIDIA', 'GLCache'),
    os.path.join(user_profile, 'AppData', 'Local', 'NVIDIA', 'DXCache'),
    os.path.join(system_root, 'LiveKernelReports')
]

total_deleted_size = 0

def clear_folder(folder_path):
    total_size = 0  
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    total_size += os.path.getsize(file_path)
                    os.unlink(file_path)  
                elif os.path.isdir(file_path):
                    total_size += get_directory_size(file_path)  
                    shutil.rmtree(file_path) 
                print(f'[Done] {file_path}')
            except Exception:
                continue
    return total_size

def flush_dns():
    try:
        print()
        print('[Clearing] DNS cache')
        subprocess.run(['ipconfig', '/flushdns'], check=True)
        print()
        print('[Done] Flushed DNS cache')
    except subprocess.CalledProcessError as e:
        print(f'[Error] Executing ipconfig /flushdns: {e}')
        
def get_directory_size(directory_path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(directory_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB")
    i = int((len(str(size_bytes)) - 1) // 3)  
    p = 1024 ** i
    size = round(size_bytes / p, 2)
    return f"{size} {size_name[i]}"

for folder in folders_to_clear:
    print(f"[Clearing] {folder}")
    total_deleted_size += clear_folder(folder)
    
flush_dns()

print(f"\nTotal size of deleted files: {convert_size(total_deleted_size)}")