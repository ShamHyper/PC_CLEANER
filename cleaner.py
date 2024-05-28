import os
import psutil

disks = psutil.disk_partitions()

tfc_before = 0
tfc_after = 0
tfc = 0

for disk in disks:
    usage = psutil.disk_usage(disk.mountpoint)
    tfc_before += usage.free

### PC_INFO legacy block
def clear():
    print('\033[37m')
    os.system('cls' if os.name == 'nt' else 'clear')

yep = ["Yes", "yes", "Y", "y", "Да", "да", "1"]
user_folder = os.path.expanduser('~')
### End of PC_INFO legacy block

print("Do you want to clear temp files?")
temp_need = False
temp_check = input("Type [Yes/yes/Y/y] or press Enter to exit: ")

if temp_check in yep:
    temp_need = True
else:
    temp_need = False

clear()

if temp_need == True:
    def clean_win_temp():
        Wtemp_path = os.path.expanduser('~\\Windows\\Temp')
        for root, dirs, files in os.walk(Wtemp_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except (PermissionError, FileExistsError, FileNotFoundError):
                    pass
            for file in files:
                Wtemp_path = os.path.join(root, file)
                try:
                    os.mkdir(Wtemp_path)
                except (PermissionError, FileNotFoundError, FileExistsError):
                    pass

    def clean_temp_files(root_dir):
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(subdir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    if os.path.isdir(file_path):
                        os.rmdir(file_path)
                except (PermissionError, FileNotFoundError, FileExistsError, NotADirectoryError):
                    pass

    def clean_temp_directory():
        temp_dir = os.getenv('temp')
        cache_dir = os.path.expanduser('~\\AppData\\Local\\Temp')
        old_updates_dir = os.path.join(os.getenv('SYSTEMDRIVE'), 'Windows', 'SoftwareDistribution', 'Download')
        hiberfil_sys_path = os.path.join('C:', os.sep, 'hiberfil.sys')
        lkr_dir = os.path.join('C:', os.sep, 'Windows', 'LiveKernelReports')
        rempls_dir = os.path.join('C:', os.sep, 'Program Files', 'empl')
        for dir_path in (temp_dir, cache_dir, old_updates_dir, hiberfil_sys_path, lkr_dir, rempls_dir):
            clean_temp_files(dir_path)

    def clear_nvidia_cache():
        nvidia_path_1 = os.path.join(user_folder, "AppData", "Local", "NVIDIA", "DXCache")
        nvidia_path_2 = os.path.join(user_folder, "AppData", "Local", "NVIDIA", "GLCache")
        for dir_path in (nvidia_path_1, nvidia_path_2):
            clean_temp_files(dir_path)

    def ultradef():
        clean_win_temp()
        clean_temp_directory()
        clear_nvidia_cache()
    
    ultradef()

    for disk in disks:
        usage = psutil.disk_usage(disk.mountpoint)
        tfc_after += usage.free

    tfc = (tfc_after - tfc_before)/1024**3
    tfc_small = (tfc_after - tfc_before)/1024**2

    if tfc > 0.1:
        print(f"Total size of deleted files: {round(tfc, 2)} GB")
    else:
        if tfc_small > 0:
            print(f"Total size of deleted files: {round(tfc_small)} MB")
        else: 
            print("Failed to clean your already perfectly cleaned PC!")

    print("")
    input("Press Enter to exit...")