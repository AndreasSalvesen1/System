import os
import platform
import subprocess
import shutil
import sys
import filecmp

GLOBAL_SCRIPT_PATH = os.path.expanduser("~/.local/bin/arch.py")
IMAGE_NAME = "arch-hyprland-desktop"

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
        input("Press Enter to continue anyway...")
    else:
        print("[!] Please install Docker manually for your platform.")
        sys.exit(1)

def build_image():
    print("[*] Building Arch Hyprland Docker image (this may take a while)...")
    dockerfile_path = os.path.expanduser("~/ws/System/Docker/Programfiler/Dockerfile.hypr")
    subprocess.run(["docker", "build", "-t", IMAGE_NAME, "-f", dockerfile_path, os.path.dirname(dockerfile_path)], check=True)
    print("[✓] Image built successfully.")

def write_dockerfile():
    dockerfile = """<insert full Dockerfile string here>"""
    output_path = os.path.expanduser("~/ws/System/Docker/Dockerfile.hypr")
    with open(output_path, "w") as f:
        f.write(dockerfile)
