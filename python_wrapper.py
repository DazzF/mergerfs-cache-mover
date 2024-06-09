import os
import sys
import subprocess
from pathlib import Path

def activate_virtualenv(venv_path):
    venv_bin = None
    if sys.platform == "win32":
        venv_bin = next((venv_path / "Scripts").glob("python.exe"), None)
    else:
        venv_bin = next((venv_path / "bin").glob("python*"), None)

    if not venv_bin:
        print(f"Python executable not found in virtual environment: {venv_path}")
        return False

    os.environ["PATH"] = f"{venv_bin.parent}:{os.environ['PATH']}"
    return True

def main():
    venv_path = Path(__file__).resolve().parent / ".venv"

    if len(sys.argv) < 2:
        print("Usage: python backup_wrapper.py script_name.py [args...]")
        sys.exit(1)

    script_to_run = Path(sys.argv[1])

    if not script_to_run.is_file():
        print(f"Script not found: {script_to_run}")
        sys.exit(1)

    if not activate_virtualenv(venv_path):
        sys.exit(1)

    try:
        script_args = [str(script_to_run)]
        script_args.extend(sys.argv[2:])  # Add all arguments after the script name
        subprocess.run(["python"] + script_args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while running the script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
