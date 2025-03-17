import os
import shutil
import subprocess
from colorama import init, Fore, Style

init()

print()
print(f"{Fore.RED}▒▒▒▒▒▒▒▒▒▒▒▄▄▄▄░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒▒▒▒▒▒▒▒▒▄██████▒▒▒▒▒▄▄▄█▄▒▒▒▒▒▒▒▒▒▒")
print("▒▒▒▒▒▒▒▄██▀░░▀██▄▒▒▒▒████████▄▒▒▒▒▒▒")
print("▒▒▒▒▒▒███░░░░░░██▒▒▒▒▒▒█▀▀▀▀▀██▄▄▒▒▒")
print("▒▒▒▒▒▄██▌░░░░░░░██▒▒▒▒▐▌▒▒▒▒▒▒▒▒▀█▄▒")
print("▒▒▒▒▒███░░▐█░█▌░██▒▒▒▒█▌▒▒▒▒▒▒▒▒▒▒▀▌")
print("▒▒▒▒████░▐█▌░▐█▌██▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒▒▒▐████░▐░░░░░▌██▒▒▒█▌▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒▒▒▒████░░░▄█░░░██▒▒▐█▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒▒▒▒████░░░██░░██▌▒▒█▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒▒▒▒████▌░▐█░░███▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒▒▒▒▐████░░▌░███▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒▒▒▒▒████░░░███▒▒▒▒█▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒▒▒██████▌░████▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒▐████████████▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("▒█████████████▄████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("██████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("██████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("█████████████████▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("█████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("████████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒")
print("------------------------------------")
print("          PC_CLEANER v1.1")
print(f"------------------------------------{Style.RESET_ALL}")


BASE_FOLDERS = [
    ("System Temp", os.path.join(os.getenv('SystemRoot'), 'Temp'), 
        "Temporary system files", False),
    ("User Temp", os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'Temp'),
        "Temporary user files", False),
    ("Windows Updates", os.path.join(os.getenv('SystemRoot'), 'SoftwareDistribution', 'Download'),
        "Windows Update downloads", False),
    ("Prefetch", os.path.join(os.getenv('SystemRoot'), 'Prefetch'),
        "System prefetch files (may slow initial program loading if cleared)", True),
    ("NVIDIA GL Cache", os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'NVIDIA', 'GLCache'),
        "NVIDIA OpenGL cache (may cause temporary shader recompilation)", True),
    ("NVIDIA DX Cache", os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'NVIDIA', 'DXCache'),
        "NVIDIA DirectX cache (may cause temporary graphics reload)", True),
    ("Live Kernel Reports", os.path.join(os.getenv('SystemRoot'), 'LiveKernelReports'),
        "System diagnostic reports", False),
    ("Internet Cache", os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'Microsoft', 'Windows', 'INetCache'),
        "Internet Explorer and Edge browser cache", False),
    ("Windows.old", os.path.join(os.getenv('SystemRoot'), '..', 'Windows.old'),
        "Previous Windows installation files (removes rollback option)", False),
    ("Recycle Bin", os.path.join(os.getenv('SystemDrive'), '$Recycle.Bin'),
        "Files in the Recycle Bin (permanent deletion)", True),
    ("Event Logs", os.path.join(os.getenv('SystemRoot'), 'System32', 'winevt', 'Logs'),
        "Windows event log files (system and application logs)", False),
    ("Thumbnail Cache", os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'Microsoft', 'Windows', 'Explorer'),
        "Thumbnail cache for file explorer (will regenerate on demand)", False),
    ("Delivery Optimization", os.path.join(os.getenv('SystemRoot'), 'SoftwareDistribution', 'DeliveryOptimization'),
        "Windows Update delivery optimization cache", False),
    ("Crash Dumps", os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'CrashDumps'),
        "Application crash dump files", False)
]

def get_directory_size(directory):
    """Calculates directory size in bytes."""
    total_size = 0
    try:
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                try:
                    total_size += os.path.getsize(os.path.join(dirpath, filename))
                except OSError:
                    continue
    except OSError:
        return 0
    return total_size

def clear_folder(folder):
    """Clears a folder and returns the freed space amount, without deletion logs."""
    deleted_size = 0
    if not os.path.exists(folder):
        return 0

    for item in os.listdir(folder):
        path = os.path.join(folder, item)
        try:
            if os.path.isfile(path) or os.path.islink(path):
                deleted_size += os.path.getsize(path)
                os.unlink(path)
            elif os.path.isdir(path):
                deleted_size += get_directory_size(path)
                shutil.rmtree(path)
        except Exception:
            continue
    return deleted_size

def flush_dns():
    """Flushes DNS cache."""
    print(f"\n{Fore.CYAN}[💽] Flushing DNS cache...{Style.RESET_ALL}")
    try:
        subprocess.run(['ipconfig', '/flushdns'], check=True)
        print(f"{Fore.GREEN}[✅] DNS cache flushed successfully{Style.RESET_ALL}")
    except subprocess.CalledProcessError:
        pass

def purge_pip_cache():
    """Purges pip cache and returns freed space."""
    pip_cache_dir = os.path.join(os.getenv('USERPROFILE'), 'AppData', 'Local', 'pip', 'Cache')
    if not os.path.exists(pip_cache_dir):
        return 0

    if not get_user_confirmation("Pip Cache", "Python package manager cache"):
        print(f"{Fore.CYAN}[💽] Skipping Pip Cache{Style.RESET_ALL}")
        return 0

    print(f"\n{Fore.CYAN}[💽] Purging pip cache...{Style.RESET_ALL}")
    try:
        size_before = get_directory_size(pip_cache_dir)
        
        result = subprocess.run(['pip', 'cache', 'purge'], capture_output=True, text=True)
        
        if result.returncode == 0:
            size_after = get_directory_size(pip_cache_dir)
            freed_size = size_before - size_after
            print(f"{Fore.GREEN}[✅] Pip cache purged successfully. Freed {convert_size(freed_size)}{Style.RESET_ALL}")
            return freed_size
        else:
            print(f"{Fore.RED}[❌] Failed to purge pip cache{Style.RESET_ALL}")
            return 0
    except Exception:
        print(f"{Fore.RED}[❌] Error while purging pip cache{Style.RESET_ALL}")
        return 0

def convert_size(size_bytes):
    """Converts size to readable format."""
    if size_bytes == 0:
        return "0 B"
    units = ("B", "KB", "MB", "GB", "TB")
    unit_idx = min(len(units) - 1, int((len(str(size_bytes)) - 1) // 3))
    size = size_bytes / (1024 ** unit_idx)
    return f"{size:.2f} {units[unit_idx]}"

def get_user_confirmation(name, description):
    """Requests user confirmation."""
    print(f"\n{Fore.YELLOW}[❓] {name}: {description}{Style.RESET_ALL}")
    while True:
        choice = input(f"{Fore.WHITE}Clear this? (y/n): {Style.RESET_ALL}").lower().strip()
        if choice in ('y', 'n'):
            return choice == 'y'
        print(f"{Fore.RED}Please enter 'y' or 'n'{Style.RESET_ALL}")

def main():
    """Main cleaning loop."""
    total_deleted_size = 0
    for name, path, desc, needs_confirm in BASE_FOLDERS:
        if not os.path.exists(path):
            continue

        if needs_confirm:
            if not get_user_confirmation(name, desc):
                print(f"{Fore.CYAN}[💽] Skipping {name}{Style.RESET_ALL}")
                continue

        print(f"\n{Fore.CYAN}[💽] Cleaning {name} ({path})...{Style.RESET_ALL}")
        size = clear_folder(path)
        total_deleted_size += size
        print(f"{Fore.GREEN}[✅] Freed {convert_size(size)} from {name}{Style.RESET_ALL}")

    flush_dns()
    total_deleted_size += purge_pip_cache()
    
    # Interface footer
    print(f"\n{Fore.MAGENTA}{'═' * 50}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Total space freed: {convert_size(total_deleted_size)}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'═' * 50}{Style.RESET_ALL}")
    input(f"{Fore.WHITE}Press Enter to exit...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()