#!/usr/bin/env python3
"""
build.py — Local build helper for AutoClicker Pro
Usage: python build.py
"""

import os
import sys
import subprocess
import shutil
import platform

NAME = "AutoClickerPro"
ENTRY = "auto_clicker.py"

def run(cmd):
    print(f"\n>> {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"ERROR: command failed with code {result.returncode}")
        sys.exit(result.returncode)

def main():
    # Install pyinstaller if needed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        run(f"{sys.executable} -m pip install pyinstaller")

    # Clean old build
    for d in ["build", "dist"]:
        if os.path.exists(d):
            shutil.rmtree(d)
    for f in os.listdir("."):
        if f.endswith(".spec"):
            os.remove(f)

    # Build command
    icon_flag = ""
    system = platform.system()
    if system == "Windows" and os.path.exists("assets/icon.ico"):
        icon_flag = "--icon=assets/icon.ico"
    elif system == "Darwin" and os.path.exists("assets/icon.icns"):
        icon_flag = "--icon=assets/icon.icns"

    windowed = "--windowed" if system in ("Windows", "Darwin") else ""

    cmd = (
        f'pyinstaller --onefile {windowed} --name {NAME} {icon_flag} {ENTRY}'
    ).strip()

    run(cmd)

    # Rename output
    suffix = {"Windows": ".exe", "Darwin": "-macos", "Linux": "-linux"}.get(system, "")
    src = os.path.join("dist", NAME + (".exe" if system == "Windows" else ""))
    dst = os.path.join("dist", f"{NAME}{suffix}")
    if os.path.exists(src) and src != dst:
        os.rename(src, dst)

    print(f"\n✅  Build complete: {dst}")
    print("    Share this file — no Python installation needed to run it.")

if __name__ == "__main__":
    main()
