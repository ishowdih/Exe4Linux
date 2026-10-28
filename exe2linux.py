import argparse
import os
from pathlib import Path
import tempfile
import subprocess

SCRIPT_DIR = Path.cwd()
parser = argparse.ArgumentParser(
    description="Wrap Windows EXE files for Linux using Wine"
)

parser.add_argument(
    "-e",
    "--exe",
    help="Target EXE file",
    required=True
)

args = parser.parse_args()
exe_file = args.exe
file_name = os.path.splitext(os.path.basename(exe_file))[0]
print(f"Target EXE: {exe_file}")
print(f"Linux File will be on: {SCRIPT_DIR}/dist/{file_name}")

def get_file_path():
  print("INFO: Getting the file path...")
  
  try:
    return SCRIPT_DIR + "/dist/" + file_name
  except Exception as e:
    print(f"Unknown & Unexpected Err: {e}")
    return None

def get_exe_file_path():
  print("INFO: Getting the path of EXE File...")
  
  try:
    return SCRIPT_DIR + exe_file
  except Exception as e:
    print(f"Unknown & Unexpected Err: {e}")
    return None

exepath = get_exe_file_path()
linux_file = get_file_path()

with open (exepath, "r", encoding="utf-8") as f:
  inside_exe = f.read()

# Going to make the rest soon, sleepy now.
