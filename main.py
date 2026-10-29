import os
import exe4linux
import sys

from sys import executable
from pathlib import Path
from shutil import which as check_install

if not exe4linux.exe_file.lower().endswith(".exe"):
    exe4linux.msgs.err(f"File '{exe4linux.exe_file}' is not an EXE File.")
    print("QUITTING!")
    raise SystemExit(1)

if sys.platform == "win32":
    exe4linux.handle_win()

script_dir = str(Path.cwd())
dist_dir = script_dir + "/dist/"

inside_py = f"""
import os
from pathlib import Path
script_dir = str(Path.cwd())
data_dir = script_dir + "/data/"
exe_file =  "{exe4linux.exe_file}"
os.system(f"wine {exe4linux.data_dir}/{exe4linux.exe_file}")"""

def run():
    exe4linux.create_data()
    exe4linux.msgs.info(f"Created Data Folder at {exe4linux.data_dir}")
    if check_install("pyinstaller") is None:
        exe4linux.install_pyinstaller()
    if check_install("wine") is None:
        exe4linux.install_wine()
    with open (script_dir + "/placeholder.py", "w", encoding="utf-8") as f:
        f.write(inside_py)
        exe4linux.msgs.info("Creating Linux File...")
        exe4linux.msgs.ok("Set PyInstaller")
        exe4linux.msgs.ok("Set Paths")
        exe4linux.msgs.ok("Created placeholder.py to generate linux file")
    try:
        exe4linux.msgs.animate_info_dots("Creating Linux executable")
        os.system(f"""cd {script_dir} && {executable} -m PyInstaller --onefile --name="{exe4linux.file_name}" --distpath="{dist_dir}" placeholder.py """)
        os.system(f"""cd {script_dir} && rm placeholder.py""")
        exe4linux.msgs.info(f"Created {exe4linux.file_name} at {dist_dir}")
    except Exception as e:
        exe4linux.msgs.err(f"Unknown & Unexpected Err: {e}")
        print("QUITTING!")
        raise SystemExit(1)

if __name__ == "__main__":
    run()
