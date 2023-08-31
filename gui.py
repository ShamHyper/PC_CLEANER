import os
import psutil
import dearpygui.dearpygui as dpg

disks = psutil.disk_partitions()

tfc_before = 0
tfc = 0

for disk in disks:
    usage = psutil.disk_usage(disk.mountpoint)
    tfc_before += usage.free

### PC_INFO legacy block
def clear():
    print('\033[37m')
    os.system('cls' if os.name == 'nt' else 'clear')

user_folder = os.path.expanduser('~')
### End of PC_INFO legacy block


clear()

def clean_win_temp():
    Wtemp_path = os.path.expanduser('~\\Windows\\Temp')
    for root, dirs, files in os.walk(Wtemp_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
            except PermissionError:
                pass
            except FileNotFoundError:
                pass
            except FileExistsError:
                pass
        for file in files:
            Wtemp_path = os.path.join(root, file)
            try:
                os.mkdir(Wtemp_path)
            except PermissionError:
                pass
            except FileNotFoundError:
                pass
            except FileExistsError:
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
            except PermissionError:
                pass
            except FileNotFoundError:
                pass
            except FileExistsError:
                pass 
            except NotADirectoryError:
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

def exit_app():
    dpg.destroy_context()

def start():
    ultradef()

    progress = dpg.add_window(label="Progress:", width=500, height=60, pos=(0,85), no_move=True, no_collapse=True, no_close=True, no_resize=True)
    text_item2 = "Starting the cleanup..."  
    dpg.add_text(text_item2, parent=progress) 

    tfc_after = 0
    for disk in disks:
        usage = psutil.disk_usage(disk.mountpoint)
        tfc_after += usage.free
    tfc = (tfc_after - tfc_before)/1024**3
    tfc_small = (tfc_after - tfc_before)/1024**2

    if tfc > 0.1:
        text_item = f"Total size of deleted files: {round(tfc, 2)} GB"
    else:
        if tfc_small > 0:
            text_item = f"Total size of deleted files: {round(tfc_small)} MB"
        else: 
            text_item = "Failed to clean your already perfectly cleaned PC!"   
    my_window = dpg.add_window(label="Result:", width=500, height=60, pos=(0,85), no_move=True, no_collapse=True, no_close=True, no_resize=True) 
    dpg.add_text(text_item, parent=my_window)


dpg.create_context()
dpg.create_viewport(title='PC_CLEANER', width=501, height=214, resizable=False, vsync=True, decorated=False)
dpg.setup_dearpygui()

with dpg.window(label="PC_CLEANER Ver.0.3.2 | Made by: ShamHyper | ©Daun-Dev, 2022-2023", width=500, height=213, no_move=True, no_collapse=True, no_close=True, no_resize=True):
    dpg.add_button(label="START CLEANING", callback=start)
    dpg.add_button(label="EXIT", callback=exit_app)


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
