import argparse
import os
import tempfile
import subprocess
import shutil

from colorama import Fore, Style, init
from pathlib import Path
from pyfiglet import figlet_format
from sys import platform
init(autoreset=True)

def info(message):
    print(f"[{Fore.GREEN}INFO{Style.RESET_ALL}] {message}")

def err(message):
  print(f"[{Fore.RED}ERROR{Style.RESET_ALL}] {message}")

def ok(message):
  print(f"[{Fore.GREEN}OK{Style.RESET_ALL}] {message}")

#define to check if the user is on windows, going to use this in future.
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
# check if wine is installed
def install_wine():
 if not os.system("wine")==0:
  ask = input("Wine is not installed, this script needs wine to run .exe, want to download it now? (Y/n) ").lower().strip()
  if ask.startswith("y"):
    os.system("sudo pacman -S --noconfirm wine ")
  elif ask.startswith("n"):
    print("Okay, but you can't run this script without wine.")
    print("QUITTING!")
    raise SystemExit("Wine isn't installed.")
  else:
    print("answer with 'y' or 'n' only.")
    print("QUITTING!")
    raise SystemExit("Invalid input.")
  
args = parser.parse_args()
exe_file = args.exe
exe_to_use_on_data = SCRIPT_DIR + "/" + exe_file
file_name = os.path.splitext(os.path.basename(exe_file))[0]
startup_text = figlet_format("EXE2LINUX")

colors = [Fore.RED, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.WHITE]
info(f"Target EXE: {exe_file}")
info(f"Linux File will be on: {SCRIPT_DIR}/dist/{file_name}")

class get_path:
 @staticmethod
 def get_file_path():
  info("Getting the file path...")
  try:
    return SCRIPT_DIR + "/dist/" + file_name
  except Exception as e:
    err(f"Unknown & Unexpected Err: {e}")
    return None
  
 @staticmethod
 def get_exe_file_path():
  info("Getting the path of EXE File...")
  try:
    return SCRIPT_DIR + "/" + exe_file
  except Exception as e:
    err(f"Unknown & Unexpected Err: {e}")
    return None
  
gpath = get_path
exepath = gpath.get_exe_file_path()
linux_file = gpath.get_file_path()
ok("Got the path of EXE File.")
ok("Got the file path.")
data_dir = SCRIPT_DIR + "/data/"

with open (exepath, "r", encoding="utf-8") as f:
  inside_exe = f.read()

def create_data():
  os.makedirs("data", exist_ok=True)
  shutil.copy2(exe_to_use_on_data, data_dir)

def run_exe():
 create_data()
 with tempfile.NamedTemporaryFile(suffix=".exe", dir=data_dir, mode="wb") as f:
     f.write(inside_exe)
     f.flush()
     subprocess.run(["wine", f.name])