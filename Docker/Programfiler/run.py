#!/usr/bin/env python3
import os
import subprocess
import time
import shutil
import sys

from Programfiler.gui import kill_existing_xephyr, monitor_shutdown_signal

IMAGE_NAME = "arch-hyprland-desktop"
VOLUME_NAME = "hypr-home"
EXITFLAG_PATH = os.path.expanduser("~/.cache/exitflag")

def run_container():
    kill_existing_xephyr(":2")

    print("[*] Cleaning up any previous container...")
    subprocess.run(["docker", "rm", "-f", "arch-hyprland"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("[*] Starting fullscreen Xephyr window...")
    xephyr = subprocess.Popen([
        "Xephyr", ":2", "-fullscreen", "-screen", "0x0", "-br", "-ac", "-noreset", "-extension", "MIT-SHM"
    ])
    time.sleep(2)

    print("[*] Granting X access to local user...")
    subprocess.run("xhost +SI:localuser:$(whoami)", shell=True)

    print("[*] Creating volume if it doesn't exist...")
    subprocess.run(["docker", "volume", "create", VOLUME_NAME], stdout=subprocess.DEVNULL)

    print("[*] Ensuring exitflag file exists...")
    os.makedirs(os.path.dirname(EXITFLAG_PATH), exist_ok=True)
    try:
        if os.path.exists(EXITFLAG_PATH):
            os.remove(EXITFLAG_PATH)
        with open(EXITFLAG_PATH, "w") as f:
            f.write("")
    except Exception as e:
        print(f"[!] Failed to ensure clean {EXITFLAG_PATH}: {e}")
        sys.exit(1)

    print("[*] Running container with DISPLAY=:2")
    container = subprocess.Popen([
        "docker", "run",
        "-e", "DISPLAY=:2",
        "-e", "LIBGL_ALWAYS_SOFTWARE=1",
        "-e", "KITTY_DISABLE_WAYLAND=1",
        "-v", "/tmp/.X11-unix:/tmp/.X11-unix",
        "-v", f"{os.path.dirname(EXITFLAG_PATH)}:/home/user/.cache",
        "-v", f"{VOLUME_NAME}:/home/user",
        "--name", "arch-hyprland",
        IMAGE_NAME
    ])

    monitor_shutdown_signal(xephyr, container)