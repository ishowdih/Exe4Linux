import argparse
import os
import shutil
import sys
import time

from colorama import Fore, Style, init
from pathlib import Path
from pyfiglet import figlet_format
from sys import platform
init(autoreset=True)

class messages:
 def info(message):
    print(f"[{Fore.GREEN}INFO{Style.RESET_ALL}] {message}")

 def err(message):
  print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] {message}")

 def ok(message):
  print(f"{Style.DIM}[{Fore.GREEN}OK{Style.RESET_ALL}{Style.DIM}] {message}{Style.RESET_ALL}")

 def animate_dots(message, duration=3):
    for i in range(duration):
        dots = "." * ((i % 3) + 1)
        sys.stdout.write(f"\r{message}{dots:<3}")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\n")

 def animate_info_dots(message, duration=3):
    for i in range(duration):
       dots = "." * ((i % 3) + 1)
       sys.stdout.write(f"\r[{Fore.GREEN}INFO{Style.RESET_ALL}] {message}{dots:<3}")
       sys.stdout.flush()
       time.sleep(1)
    sys.stdout.write("\n")


#define to check if the user is on windows
def check_win():
 if platform == "win32":
  print("This is Linux only.")
  print("QUITTING!")
  raise SystemExit("You can't run this on Windows.")

SCRIPT_DIR = str(Path(__file__).resolve().parent)
parser = argparse.ArgumentParser(
    description="Wrap Windows EXE files for Linux using Wine"
)

parser.add_argument(
    "-e",
    "--exe",
    help="Target EXE file",
    required=True
)
#define to install wine
def install_wine():
    ask = input("Wine is not installed, this script needs wine to run .exe, want to download it now? (Y/n) ").lower().strip()
    if ask.startswith("y"):
        distro = detect_distro()
        if distro == "arch":
            os.system("sudo pacman -S --noconfirm wine")
        elif distro == "debian":
            os.system("sudo apt update && sudo apt install -y wine")
        else:
            print(f"Unsupported distro: {distro}. Install wine manually.")
            raise SystemExit(1)
    elif ask.startswith("n"):
        print("Okay, but you can't run this script without wine.")
        print("QUITTING!")
        raise SystemExit("Wine isn't installed.")
    else:
        print("answer with 'y' or 'n' only.")
        print("QUITTING!")
        raise SystemExit("Invalid input.")


def install_pyinstaller():
  ask = input("PyInstaller is not installed. This script needs PyInstaller to create Linux executable.\nWant to download it now? (Y/n) ").lower().strip()
  if ask.startswith("y"):
    os.system("python -m pip install pyinstaller ")
  elif ask.startswith("n"):
    print("Okay, but you can't run this script without PyInstaller.")
    print("QUITTING!")
    raise SystemExit("PyInstaller isn't installed.")
  else:
    print("answer with 'y' or 'n' only.")
    print("QUITTING!")
    raise SystemExit("Invalid input.")

def detect_distro():
    distro = ""
    try:
        with open("/etc/os-release", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("ID="):
                    distro = line.strip().split("=", 1)[1].strip('"')
                    break
    except FileNotFoundError:
        return "unknown"

    if distro in ("arch", "manjaro", "endeavouros", "cachyos"):
        return "arch"
    if distro in ("ubuntu", "debian", "linuxmint", "pop", "kali"):
        return "debian"
    return distro  

#IMPORTANT, DONT DELETE!
args = parser.parse_args()
exe_file = args.exe
exe_to_use_on_data = SCRIPT_DIR + "/" + exe_file
file_name = os.path.splitext(os.path.basename(exe_file))[0]
startup_text = figlet_format("EXE4LINUX")
colors = [Fore.RED, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.WHITE]
msgs = messages
os.system("clear")
print(startup_text)
print("     V0.0.1 - Eymorty\n")
msgs.info(f"Checking if {exe_file} really exists in the current directory...")
if not os.path.exists(exe_file):
  msgs.err(f"File '{exe_file}' does not exist in the current directory.")
  print("QUITTING!")
  raise SystemExit(1)
elif os.path.exists(exe_file):
  msgs.ok(f"File '{exe_file}' exists.")
msgs.info(f"Target EXE: {exe_file}")
msgs.info(f"Linux File will be on: {SCRIPT_DIR}/dist/{file_name}")

class get_path:
 @staticmethod
 def get_file_path():
  msgs.info("Getting the file path...")
  try:
    return SCRIPT_DIR + "/dist/" + file_name
  except Exception as e:
    msgs.err(f"Unknown & Unexpected Err: {e}")
    return None
  
 @staticmethod
 def get_exe_file_path():
  msgs.info("Getting the path of EXE File...")
  try:
    return SCRIPT_DIR + "/" + exe_file
  except Exception as e:
    msgs.err(f"Unknown & Unexpected Err: {e}")
    return None
  
gpath = get_path
exepath = gpath.get_exe_file_path()
linux_file = gpath.get_file_path()
msgs.ok("Got the path of EXE File.")
msgs.ok("Got the file path.")
data_dir = SCRIPT_DIR + "/data/"

def create_data():
  os.makedirs("data", exist_ok=True)
  os.makedirs("dist", exist_ok=True)
  shutil.copy2(exe_to_use_on_data, data_dir)

