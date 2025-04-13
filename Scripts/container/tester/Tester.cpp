// Tester at menyen fungerer korrekt
#include <iostream>
#include "container.h"

using namespace std;

void testMeny(){
    cout 
    << endl
    << "Menyen fungerer korrekt ...";
}

// ✅ Updated main function to handle restoration & reinstallation
void runContainer() {
    std::string osType = detectOS();
    std::cout << "🌍 Operating System: " << osType << std::endl;

    std::cout << "Choose an option:\n1 - Install Docker\n2 - Remove Docker\n3 - Exit\nEnter your choice: ";
    int choice;
    std::cin >> choice;

    if (choice == 3) {
        std::cout << "🚪 Exiting...\n";
        return;
    }

    if (!isDockerInstalled()) {
        std::cout << "⚠️ Docker is NOT installed. Proceeding with installation...\n";

        if (osType == "Linux") {
            // ✅ If Docker binary is missing, try to restore it
            if (restoreDockerBinary()) {
                std::cout << "🔄 Verifying Docker installation...\n";
                if (isDockerInstalled()) {
                    std::cout << "✅ Docker restored successfully!\n";
                    return;
                }
            }

            // ✅ If restoration fails, attempt a full reinstallation
            std::cout << "❌ Could not restore Docker binary. Attempting reinstallation...\n";
            reinstallDockerLinux();
        } else if (osType == "macOS") {
            installDockerMac();
        } else if (osType == "Windows") {
            installDockerWindows();
        }
    } else {
        std::cout << "✅ Docker is already installed!\n";
        if (choice == 2) {
            std::cout << "⚠️ Proceeding with Docker removal...\n";
            if (osType == "Linux") removeDockerLinux();
            else if (osType == "macOS") removeDockerMac();
            else if (osType == "Windows") removeDockerWindows();
        } else {
            std::cout << "Docker is already installed. No need to install again.\n";
        }
    }
}