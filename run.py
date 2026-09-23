import subprocess
import sys

subprocess.Popen(
    [
        "cmd.exe",
        "/k",
        sys.executable,
        "VM.py"
    ],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)