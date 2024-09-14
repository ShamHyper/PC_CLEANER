import os
import shutil
import subprocess

### CLEANER 1.x ###

# Function to clear the contents of a folder
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove file or symbolic link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove folder and its contents
                print(f'[Done] {file_path}')
            except Exception:
                continue

# Get system paths
user_profile = os.getenv('USERPROFILE')  # Path to the user directory
system_root = os.getenv('SystemRoot')  # Path to the Windows directory

# List of folders to clear their contents
folders_to_clear = [
    os.path.join(system_root, 'Temp'),
    os.path.join(user_profile, 'AppData', 'Local', 'Temp'),
    os.path.join(system_root, 'SoftwareDistribution', 'Download'),
    os.path.join(system_root, 'Prefetch'),
    os.path.join(user_profile, 'AppData', 'Local', 'NVIDIA', 'GLCache'),
    os.path.join(user_profile, 'AppData', 'Local', 'NVIDIA', 'DXCache'),
    os.path.join(system_root, 'LiveKernelReports')
]

# Loop to clear the contents of each folder
for folder in folders_to_clear:
    print(f"[Clearing] {folder}")
    clear_folder(folder)

# Command to flush DNS cache
def flush_dns():
    try:
        print()
        print('[Clearing] DNS cache')
        subprocess.run(['ipconfig', '/flushdns'], check=True)
        print()
        print('[Done] Flushed DNS cache')
    except subprocess.CalledProcessError as e:
        print(f'[Error] Еxecuting ipconfig /flushdns: {e}')

# Execute DNS flush command
flush_dns()