import os
import sys
import time
import shutil
import subprocess

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
GRAY = "\033[90m"
RESET = "\033[0m"

def line():
    print(f"{CYAN}{'=' * 60}{RESET}")

def header():
    os.system("cls" if os.name == "nt" else "clear")

    line()
    print(f"""{GRAY}
          

                         ░██                        ░██                          ░██
                         ░██                                                        
 ░███████   ░███████  ░████████  ░███████  ░██░████ ░██ ░██████        ░██████   ░██
░██        ░██    ░██    ░██    ░██    ░██ ░███     ░██      ░██            ░██  ░██
 ░███████  ░██    ░██    ░██    ░█████████ ░██      ░██ ░███████       ░███████  ░██
       ░██ ░██    ░██    ░██    ░██        ░██      ░██░██   ░██      ░██   ░██  ░██
 ░███████   ░███████      ░████  ░███████  ░██      ░██ ░█████░██ ░██  ░█████░██ ░██

                                                                                           

        Cybersecurity Toolkit Installer

{RESET}""")
    line()

def step(message):
    print(f"\n{CYAN}➜ {message}{RESET}")

def success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def warning(message):
    print(f"{YELLOW}! {message}{RESET}")

def error(message):
    print(f"{RED}✗ {message}{RESET}")

header()

step("Checking Python version...")

time.sleep(0.5)

if sys.version_info < (3, 10):
    error("Python 3.10 or newer is required.")
    sys.exit(1)

success(f"Python {sys.version.split()[0]} detected")

step("Installing dependencies...")

try:

    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-r",
        "requirements.txt"
    ])

    success("Dependencies installed")

except subprocess.CalledProcessError:

    error("Failed to install requirements.")
    sys.exit(1)

step("Creating project folders...")

folders = [
    "uploads",
    "logs",
    "temp"
]

for folder in folders:

    os.makedirs(folder, exist_ok=True)

success("Folders ready")

step("Checking configuration...")

if not os.path.exists(".env"):

    if os.path.exists(".env.example"):

        shutil.copy(".env.example", ".env")

        success(".env created from template")

    else:

        warning(".env.example not found")

else:

    success(".env already exists")

line()

print(f"""{GREEN}

Soteria has been installed successfully!

Next steps:

1. Add your Gemini API key to .env

2. Start the server:

       python app.py

3. Open:

       http://127.0.0.1:5000

Welcome to Soteria!

{RESET}""")

line()