from Programfiler.run import *
from Programfiler.setup import *
from Programfiler.gui import *

sync_global_script()
if not docker_installed():
    install_docker()
if shutil.which("docker") is None:
    print("❌ Docker is still not found after install.")
    sys.exit(1)

build_image()
run_container()
os.system("clear")