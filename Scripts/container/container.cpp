#include <iostream>
#include <cstdlib>
#include <string>
#include "container.h"

#ifdef _WIN32
#include <windows.h>
#endif

std::string detectOS() {
#ifdef _WIN32
    return "Windows";
#elif __APPLE__
    return "macOS";
#elif __linux__
    return "Linux";
#else
    return "Unknown";
#endif
}

bool isDockerInstalled() {
#ifdef _WIN32
    return system("docker --version >nul 2>&1") == 0;
#else
    return system("docker --version > /dev/null 2>&1") == 0;
#endif
}

// ✅ Check if WSL 2 is enabled (Windows only)
bool isWSL2Enabled() {
#ifdef _WIN32
    return system("wsl --list --verbose | findstr \"WSL 2\" >nul 2>&1") == 0;
#else
    return false;
#endif
}

// ✅ Enable WSL 2 on Windows
void enableWSL2() {
    std::cout << "🔧 Enabling WSL 2 on Windows...\n";
    int result = system("wsl --install");

    if (result == 0) {
        std::cout << "✅ WSL 2 installed successfully! Setting as default...\n";
        system("wsl --set-default-version 2");
    } else {
        std::cerr << "❌ Failed to install WSL 2. Please install it manually.\n";
    }
}

// ✅ Restore missing Docker binary (Linux)
bool restoreDockerBinary() {
    std::cout << "🔍 Searching for missing Docker binary...\n";
    int result = system("sudo find /usr -name docker -type f > /tmp/docker_location 2>/dev/null");

    if (result != 0) {
        std::cerr << "❌ No alternative Docker binary found.\n";
        return false;
    }

    FILE *file = fopen("/tmp/docker_location", "r");
    if (file == nullptr) {
        std::cerr << "❌ Failed to read Docker binary location.\n";
        return false;
    }

    char dockerPath[256];
    if (fgets(dockerPath, sizeof(dockerPath), file) != nullptr) {
        std::string dockerBinaryPath(dockerPath);
        dockerBinaryPath.erase(dockerBinaryPath.find_last_not_of("\n") + 1);

        std::cout << "✅ Found Docker binary at: " << dockerBinaryPath << "\n";
        std::cout << "🔗 Creating symlink to /usr/bin/docker...\n";

        std::string linkCommand = "sudo ln -s " + dockerBinaryPath + " /usr/bin/docker";
        int linkResult = system(linkCommand.c_str());

        if (linkResult == 0) {
            std::cout << "✅ Docker binary restored successfully!\n";
            fclose(file);
            return true;
        } else {
            std::cerr << "❌ Failed to create symlink.\n";
        }
    }

    fclose(file);
    return false;
}

// ✅ Reinstall Docker if completely broken (Linux)
void reinstallDockerLinux() {
    std::cout << "🔄 Reinstalling Docker on Linux...\n";
    system("sudo apt purge -y docker-ce docker-ce-cli docker-ce-rootless-extras docker-compose-plugin");
    system("sudo rm -rf /var/lib/docker /var/lib/containerd");

    int installResult = system("curl -fsSL https://get.docker.com | sudo sh");

    if (installResult == 0) {
        std::cout << "✅ Docker reinstalled successfully!\n";
        system("sudo systemctl restart docker");
        system("sudo systemctl enable docker");
    } else {
        std::cerr << "❌ Failed to reinstall Docker.\n";
    }
}

// ✅ Install Docker on Linux
void installDockerLinux() {
    std::cout << "📦 Installing Docker on Linux...\n";
    int result = system("curl -fsSL https://get.docker.com | sudo sh");

    if (result == 0) {
        std::cout << "✅ Docker installed successfully on Linux!\n";
        system("sudo usermod -aG docker $USER");
        std::cout << "⚠️ You may need to log out and log back in for group changes to take effect.\n";
    } else {
        std::cerr << "❌ Failed to install Docker on Linux!\n";
    }
}

// ✅ Install Docker on macOS
void installDockerMac() {
    std::cout << "📦 Installing Docker on macOS...\n";
    int result = system("brew install --cask docker");

    if (result == 0) {
        std::cout << "✅ Docker installed successfully on macOS!\n";
    } else {
        std::cerr << "❌ Failed to install Docker on macOS! Ensure Homebrew is installed.\n";
    }
}

// ✅ Install Docker on Windows (with WSL 2 check)
void installDockerWindows() {
    std::cout << "🛠️ Checking for WSL 2...\n";

    if (!isWSL2Enabled()) {
        std::cout << "⚠️ WSL 2 is not enabled. Installing it now...\n";
        enableWSL2();
    } else {
        std::cout << "✅ WSL 2 is already enabled.\n";
    }

    std::cout << "📥 Downloading Docker Desktop installer...\n";
    int result = system("powershell -Command \"Invoke-WebRequest -Uri https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe -OutFile DockerInstaller.exe\"");

    if (result == 0) {
        std::cout << "✅ Docker installer downloaded. Running installer...\n";
        system("start DockerInstaller.exe");
        std::cout << "Follow the installation wizard to complete setup.\n";
    } else {
        std::cerr << "❌ Failed to download Docker installer on Windows!\n";
    }
}


// ✅ Remove Docker on Linux
void removeDockerLinux() {
    std::cout << "🛑 Removing Docker from Linux...\n";
    system("sudo systemctl stop docker");
    system("sudo systemctl stop containerd");
    system("sudo apt-get remove -y docker docker-engine docker.io containerd runc && sudo apt-get autoremove -y");
    system("sudo snap remove docker 2>/dev/null");
    system("flatpak uninstall -y com.docker.docker 2>/dev/null");
    system("sudo rm -rf /var/lib/docker /var/lib/containerd /etc/docker $HOME/.docker");
    system("sudo rm -rf /usr/bin/docker* /usr/local/bin/docker* /usr/lib/docker");

    if (system("docker --version > /dev/null 2>&1") != 0) {
        std::cout << "✅ Docker successfully removed from Linux.\n";
    } else {
        std::cerr << "❌ Docker removal failed! Some residual files may still exist.\n";
    }
}

// ✅ Remove Docker on macOS
void removeDockerMac() {
    std::cout << "🛑 Removing Docker from macOS...\n";
    int result = system("brew uninstall --cask docker");

    if (result == 0) {
        std::cout << "✅ Docker removed successfully from macOS.\n";
    } else {
        std::cerr << "❌ Failed to remove Docker from macOS! Ensure Homebrew is installed.\n";
    }
}

// ✅ Remove Docker on Windows
void removeDockerWindows() {
    std::cout << "🛑 Removing Docker Desktop from Windows...\n";
    int result = system("powershell -Command \"winget uninstall -e --id Docker.DockerDesktop\"");

    if (result == 0) {
        std::cout << "✅ Docker Desktop removed successfully from Windows.\n";
    } else {
        std::cerr << "❌ Failed to remove Docker Desktop from Windows! Try uninstalling manually.\n";
    }
}





// // ✅ Updated main function to handle restoration & reinstallation
// int runContainer() {
//     std::string osType = detectOS();
//     std::cout << "🌍 Operating System: " << osType << std::endl;

//     std::cout << "Choose an option:\n1 - Install Docker\n2 - Remove Docker\n3 - Exit\nEnter your choice: ";
//     int choice;
//     std::cin >> choice;

//     if (choice == 3) {
//         std::cout << "🚪 Exiting...\n";
//         return 0;
//     }

//     if (!isDockerInstalled()) {
//         std::cout << "⚠️ Docker is NOT installed. Proceeding with installation...\n";

//         if (osType == "Linux") {
//             // ✅ If Docker binary is missing, try to restore it
//             if (restoreDockerBinary()) {
//                 std::cout << "🔄 Verifying Docker installation...\n";
//                 if (isDockerInstalled()) {
//                     std::cout << "✅ Docker restored successfully!\n";
//                     return 0;
//                 }
//             }

//             // ✅ If restoration fails, attempt a full reinstallation
//             std::cout << "❌ Could not restore Docker binary. Attempting reinstallation...\n";
//             reinstallDockerLinux();
//         } else if (osType == "macOS") {
//             installDockerMac();
//         } else if (osType == "Windows") {
//             installDockerWindows();
//         }
//     } else {
//         std::cout << "✅ Docker is already installed!\n";
//         if (choice == 2) {
//             std::cout << "⚠️ Proceeding with Docker removal...\n";
//             if (osType == "Linux") removeDockerLinux();
//             else if (osType == "macOS") removeDockerMac();
//             else if (osType == "Windows") removeDockerWindows();
//         } else {
//             std::cout << "Docker is already installed. No need to install again.\n";
//         }
//     }

//     return 0;
// }