import os
import subprocess
import time
import signal

EXITFLAG_PATH = os.path.expanduser("~/.cache/exitflag")

def kill_existing_xephyr(display_number=":2"):
    d = display_number.lstrip(":")
    socket_file = f"/tmp/.X11-unix/X{d}"
    lock_file = f"/tmp/.X{d}-lock"

    print(f"[*] Dreper Xephyr-prosesser for display {display_number}...")

    try:
        output = subprocess.check_output(["lsof", "|", "grep", f"X{d}"], shell=True).decode().splitlines()
        for line in output:
            if f"/tmp/.X11-unix/X{d}" in line:
                pid = int(line.split()[1])
                print(f"[*] Dreper prosess {pid} som holder display {display_number}")
                os.kill(pid, signal.SIGKILL)
    except Exception:
        print("[=] Ingen aktive prosesser funnet via lsof.")

    for path in [socket_file, lock_file]:
        if os.path.exists(path):
            print(f"[*] Fjerner {path}")
            os.remove(path)

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
