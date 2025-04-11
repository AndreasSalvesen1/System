#!/usr/bin/env python3
import os
import platform
import subprocess
import shutil
import sys
import time
import filecmp

GLOBAL_SCRIPT_PATH = os.path.expanduser("~/.local/bin/arch.py")
IMAGE_NAME = "arch-hyprland-desktop"
VOLUME_NAME = "hypr-home"
EXITFLAG_PATH = os.path.expanduser("~/.cache/exitflag")

def sync_global_script():
    script_path = os.path.realpath(__file__)
    if not os.path.exists(GLOBAL_SCRIPT_PATH) or not filecmp.cmp(script_path, GLOBAL_SCRIPT_PATH):
        print("[*] Syncing global script to:", GLOBAL_SCRIPT_PATH)
        shutil.copy(script_path, GLOBAL_SCRIPT_PATH)
        subprocess.run(["chmod", "+x", GLOBAL_SCRIPT_PATH])
        print("[✓] Global script updated.")

def docker_installed():
    return shutil.which("docker") is not None

def install_docker():
    os_type = platform.system().lower()
    if os_type == "linux":
        print("[+] Installing Docker using official script for Linux...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run(["sudo", "apt", "install", "-y", "curl", "ca-certificates", "gnupg", "lsb-release"], check=True)
        subprocess.run(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"], check=True)
        subprocess.run(["sudo", "sh", "get-docker.sh"], check=True)
        subprocess.run(["sudo", "usermod", "-aG", "docker", os.getlogin()])
        print("\n[!] Docker installed successfully. You may need to log out and log back in to apply group changes.")
        input("Press Enter to continue anyway...")
    else:
        print("[!] Please install Docker manually for your platform.")
        sys.exit(1)

def build_image():
    print("[*] Building Arch Hyprland Docker image (this may take a while)...")
    dockerfile_path = os.path.expanduser("~/ws/System/Docker/Dockerfile.hypr")
    subprocess.run(["docker", "build", "-t", IMAGE_NAME, "-f", dockerfile_path, os.path.dirname(dockerfile_path)], check=True)
    print("[✓] Image built successfully.")

def write_dockerfile():
    dockerfile = f"""
FROM archlinux:latest

ENV USER=user
ENV HOME=/home/$USER

RUN pacman -Sy --noconfirm && \\
    pacman -S --noconfirm sudo git base-devel i3-wm kitty rofi waybar firefox \\
    ttf-dejavu ttf-font-awesome xorg-xhost xorg-xrandr mesa libglvnd neovim

RUN useradd -m $USER && echo "$USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER $USER
WORKDIR /home/$USER

RUN git clone https://github.com/AndreasSalvesen1/System /home/user/System || echo "[=] Repo already exists or clone failed"

COPY startup.sh /usr/local/bin/startup.sh
RUN sudo chmod +x /usr/local/bin/startup.sh
CMD ["sudo /usr/local/bin/startup.sh"]

RUN mkdir -p ~/.config/i3 && \\
    echo 'set $mod Mod4' > ~/.config/i3/config && \\
    echo 'font pango:monospace 10' >> ~/.config/i3/config && \\
    echo 'exec_always --no-startup-id env LIBGL_ALWAYS_SOFTWARE=1 KITTY_DISABLE_WAYLAND=1 kitty' >> ~/.config/i3/config && \\
    echo 'bindsym $mod+Return exec env LIBGL_ALWAYS_SOFTWARE=1 KITTY_DISABLE_WAYLAND=1 kitty' >> ~/.config/i3/config && \\
    echo 'bindsym $mod+d exec rofi -show drun' >> ~/.config/i3/config && \\
    echo 'bindsym $mod+Shift+q kill' >> ~/.config/i3/config && \\
    echo 'bindsym $mod+Shift+e exec --no-startup-id returnhost' >> ~/.config/i3/config && \\
    echo 'bindsym $mod+f fullscreen toggle' >> ~/.config/i3/config && \\
    echo 'focus_follows_mouse yes' >> ~/.config/i3/config && \\
    echo 'floating_modifier $mod' >> ~/.config/i3/config

USER root
RUN mkdir -p /usr/local/bin && \\
    bash -c 'printf "#!/bin/bash\\necho shutdown > ~/.cache/exitflag\\n" > /usr/local/bin/returnhost' && \\
    chmod +x /usr/local/bin/returnhost

USER $USER
CMD ["i3"]
"""
    output_path = os.path.expanduser("~/ws/System/Docker/Dockerfile.hypr")
    with open(output_path, "w") as f:
        f.write(dockerfile)

def monitor_shutdown_signal(xephyr_proc, container_proc):
    control_file = EXITFLAG_PATH

    print("[*] Type 'returnhost' in the Docker terminal or press Mod+Shift+e in i3 to exit.")

    try:
        while True:
            try:
                with open(control_file, "r") as f:
                    if f.read().strip() == "shutdown":
                        break
            except FileNotFoundError:
                pass
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Ctrl+C pressed, stopping...")

    print("[!] Shutdown signal received. Cleaning up...")

    try:
        subprocess.run(["docker", "stop", "arch-hyprland"], check=False)
    except Exception as e:
        print(f"[!] Error stopping container: {e}")

    try:
        xephyr_proc.kill()
    except Exception as e:
        print(f"[!] Error killing Xephyr: {e}")

    try:
        os.remove(control_file)
    except:
        pass

    os.system("clear")

def run_container():
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

if __name__ == "__main__":
    sync_global_script()
    if not docker_installed():
        install_docker()
    if shutil.which("docker") is None:
        print("❌ Docker is still not found after install.")
        sys.exit(1)

    write_dockerfile()
    build_image()
    run_container()
    os.system("clear")

