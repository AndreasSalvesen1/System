import subprocess
import os
from colorama import Fore, Back, Style
import subprocess
import os
import shutil
import time
import os
import time
import re


#KONFIGURASJON
# -----------------------------------------------------------------------------------------------------------------------------------------------------

#Konfigurasjon 1
HemmeligFilSti = "/media/andreas/UBUNTU 24_0"
IgnorerFilNavn = "IgnorerDisseFiler.txt"


#Konfigurasjon 2
Email = "andreassalvesen1@outlook.com"


# Konfigurasjon 3
GitHubUsername = "AndreasSalvesen1"


# Konfigurasjon 4
localBaseFolder = "/home/andreas/Global"
rcloneRemoteName = "OneDrive"  # The name you used during rclone config
remoteBaseFolder = "Arkiv/"

# Konfigurasjon 5
courseCodes = [
    "Home", 
    "test"
    ]



#PROGRAMFUNKSJONER
# -----------------------------------------------------------------------------------------------------------------------------------------------------

def InitialiserGlobaleFunksjoner():
    
    global NL
    global Kommando
    global PrintError
    global PrintSuccess
    global PrintResultat
    global PrintInfo
    global PrintDebug
    global PrintStepSuccess
    global PrintStepError
    global PrintMainSuccess
    global PrintMainError
    global snapshot_dir
    global check_for_changes
    
    
    def NL(AntallLinjer):
        print("\n"*AntallLinjer)
        return
    
    def Kommando(Command):
        try:
            output = subprocess.check_output(Command, shell=True, stderr=subprocess.STDOUT)
            # PrintSuccess(output.decode())
        except subprocess.CalledProcessError as e:
            PrintError("Error executing command:")
            PrintError(Command)
            PrintResultat(e.output.decode())
            return False
        return True
    
    def PrintError(tekst):
        NL(1)
        print(Fore.RED + tekst + Style.RESET_ALL)
        time.sleep(1)
        return
    
    def PrintSuccess(tekst):
        NL(1)
        print(Fore.GREEN + tekst + Style.RESET_ALL)
        time.sleep(1)
        return
    
    def PrintResultat(tekst):
        NL(1)
        print(Fore.YELLOW + tekst + Style.RESET_ALL)
        time.sleep(1)
        return
    
    def PrintInfo(tekst):
        NL(2)
        print(Fore.BLUE + tekst + Style.RESET_ALL)
        time.sleep(1)
        return
    
    def PrintDebug(tekst):
        NL(2)
        print(Fore.WHITE + tekst + Style.RESET_ALL)
        time.sleep(1)
        return
    
    def PrintStepSuccess(tekst):
        NL(2)
        print(Fore.GREEN + Back.BLUE + Style.BRIGHT + tekst + Style.RESET_ALL)
        time.sleep(1)
        return
    
    def PrintStepError(tekst):
        NL(1)
        print(Fore.RED + Back.BLUE + Style.BRIGHT + tekst + Style.RESET_ALL)
        time.sleep(1)
        return
    
    def PrintMainSuccess(tekst):
        NL(3)
        print(Fore.GREEN + Back.YELLOW + Style.BRIGHT + tekst + Style.RESET_ALL)
        time.sleep(1)
        return
    
    def PrintMainError(tekst):
        NL(2)
        print(Fore.RED + Back.YELLOW + Style.BRIGHT + tekst + Style.RESET_ALL)
        time.sleep(1)
        return
    
    def snapshot_dir(path):
        """Take a snapshot of the directory contents, including subdirectories."""
        snapshot = {}
        for root, dirs, files in os.walk(path):
            # Exclude .git directories
            if '.git' in dirs:
                dirs.remove('.git')
            for name in files:
                full_path = os.path.join(root, name)
                try:
                    stat = os.stat(full_path)
                    snapshot[full_path] = stat.st_mtime
                except FileNotFoundError:
                    # The file might have been removed between os.walk and os.stat
                    continue
                
        # print("Snapshot taken:")
        # print(snapshot)
        return snapshot
    
    def check_for_changes(initial, current):
        """Check for any changes between two snapshots."""
        removed = set(initial) - set(current)
        if removed:
            print("Changes detected:")
            return True
        for path, mtime in current.items():
            if path not in initial or initial[path] != mtime:
                print("Changes detected:")
                return True
        return False

    
    return

def SjekkMinnepinne():
    
    PrintInfo("Sjekker om USB-C minnepinne, med korrekt filsti, er tilkoblet ...")  
    def StartTest():
        try :
            global HemmeligFilSti
            FILSTI = HemmeligFilSti + "/" + IgnorerFilNavn
            # FILSTI = HemmeligFilSti + "GitHubT.txt"
            # PrintDebug(FILSTI)
            with open(FILSTI, "r") as f:
                # for line in f:
                #     IgnorerDisseFiler.append(line)
                # print("Ignorerer filene:", IgnorerDisseFiler); NL(1)
                # print("Returnerer True"); NL(1)
                HemmeligFilSti = "/media/andreas/UBUNTU 24_0"
                return True
        except FileNotFoundError as e:
            PrintError("Fil ikke funnet ...")
            PrintResultat(str(e))
            return False
        except PermissionError:
            PrintError("Ingen tilgang til filen ...")
            return False
        except Exception as e:
            PrintError("Ukjent feil oppstod ...")
            PrintResultat(e)
            return False


    if not StartTest():
        # PrintError("USB-C minnepinne ikke tilkoblet ...")
        return False
    else :
        PrintSuccess("USB-C minnepinne tilkoblet ...")
        return True

def SetupOgSyncRepoFraGitHub():
    
    def fjernSSHKeyFraAgent(HemmeligFilsti):
        
        KeyPath = os.path.join(HemmeligFilsti, "id_rsa")    
        PrintInfo("Fjerner SSH key fra agent ...")
        command = ['ssh-add', '-D', KeyPath]
        Kommando(command)
        PrintSuccess("SSH key fjernet fra agent ...")

    def SetupSSH(ssh_key_path, TempKatalog):
        
        # TempKatalog = "/home/Home/Scripts/Setup"
        # TempKatalog = "~/Home/Scripts/Setup"
        TempKatalogFil = TempKatalog + "/id_rsa"
        
        
        def removeUnusedDirectories(TempKatalog):
            
            current_time = time.time()
            period_in_seconds = 24 * 60 * 60

            for directory_name in os.listdir(TempKatalog):
                if directory_name.startswith("ssh-"):
                    directory_path = os.path.join(TempKatalog, directory_name)
                    if os.path.isdir(directory_path):
                        last_modified = os.path.getmtime(directory_path)
                        if current_time - last_modified > period_in_seconds:
                            shutil.rmtree(directory_path)
                            print(f"Removed ssh-directory not used in 1 day: {directory_path}")
        
        def copy_key_to_local(ssh_key_path):
            command = ("cp " + ssh_key_path + " " + TempKatalog)
            PrintInfo("Attempting to copy key to local directory ...")
            Kommando(command)
            PrintSuccess("SSH key copied to /tmp")
        
        def set_key_permissions():
            command = ('chmod ' + '600 ' + TempKatalogFil)
            PrintInfo("Attempting to set key permissions to 600 ...")
            Kommando(command)
            PrintSuccess(f"Permissions for {TempKatalogFil} set to 600")
            
            # command = ['chmod', '700', TempKatalog]; Kommando(command)
            # print(f"Permissions for {TempKatalog} set to 700")

        def start_ssh_agent():
            PrintInfo("Starting SSH agent ...")
            command = "eval `ssh-agent -s`"
            output = Kommando(command)
            PrintSuccess("SSH agent started ...")
            return output

        def add_key_to_ssh_agent():
            PrintInfo("Adding key to SSH agent ...")
            command = ('ssh-add ' + TempKatalogFil)
            Kommando(command)
            PrintSuccess(f"Added {TempKatalogFil} to SSH agent")
        
        def removeTempFile():
            temp_file_path = os.path.join(TempKatalog, "id_rsa")
            PrintInfo("Removing temporary keyfile ...")
            try:
                os.remove(temp_file_path)
                PrintSuccess(f"Temporary file {temp_file_path} removed ...")
            except Exception:
                pass
            
        def display_public_key(ssh_key_path):
            public_key_path = ssh_key_path + ".pub"
            PrintInfo(f"Public key:")
            command = ('cat ' + public_key_path)
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
            PrintResultat(output)
            # PrintDebug("Don't forget to add your SSH public key to your GitHub account")
        
        
        def main():
            
            removeUnusedDirectories(TempKatalog)
            # try:
            copy_key_to_local(ssh_key_path)
            set_key_permissions()
            start_ssh_agent()
            add_key_to_ssh_agent()
            removeTempFile()
            display_public_key(ssh_key_path)
            # except FileNotFoundError:
            #     return
            
        main()
        return True

    def SetupGit():
        
        def Autentiser(): 
                        
            def LoggInnTilGitHub():
                
                def getGHToken():
                    token_file_path = os.path.join(HemmeligFilSti, "GitHubT.txt")
                    with open(token_file_path, "r") as token_file:
                        token = token_file.read().strip()
                    return token 
                
                def LoggInnTilGitHubMedToken():
                    PrintInfo("Logger inn til GitHub med token ...")
                    
                    token = getGHToken()
                    command = f"echo {token} | gh auth login --with-token"
                    
                    try: 
                        Kommando(command)
                        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
                        PrintSuccess("GitHub token login successful ...")
                        return True
                    except subprocess.CalledProcessError as e:
                    # except FileNotFoundError as e:
                        PrintError("GitHub token login failed ...")
                        PrintResultat(e.output.decode())
                        return False
                
                def LoggInnTilGithubMedSSH():
                    PrintInfo("Logger inn til Git med SSH ...")
                    command = "ssh -T git@github.com"
                    
                    try :            
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
                        PrintResultat(output)
                        PrintSuccess("SSH login successful ...")
                        return True

                    except subprocess.CalledProcessError as e:
                        
                        output = e.output.decode()
                        
                        if "Hi AndreasSalvesen1! You've successfully authenticated" in output:
                            PrintSuccess("SSH login successful ...")
                            return True
                        else:
                            PrintError("SSH login failed ...")
                            PrintResultat(e.output.decode())
                            return False
                        
                def main():
                    
                    if not LoggInnTilGitHubMedToken():
                        PrintStepError("Error logging in to GitHub with token ..."); NL(0)
                        return False
                    
                    if not LoggInnTilGithubMedSSH():
                        PrintStepError("Error logging in to GitHub with SSH ..."); NL(0)
                        return False
                    
                    return True
                
                if not main():
                    PrintMainError("Error logging in to GitHub ..."); NL(0)
                    return False
                
                return True
                    
            def SettGitBrukernavnOgEmail():
                
                PrintInfo("Konfigurerer Git ...")
                try:
                    subprocess.check_call(["git", "config", "--global", "user.name", GitHubUsername])
                    subprocess.check_call(["git", "config", "--global", "user.Email", Email])
                    PrintSuccess(f"Git user.name and user.email set to {GitHubUsername} and {Email}, respectively ...")
                    return True
                except subprocess.CalledProcessError as e:
                    NL(0)
                    PrintError("Error setting Git GitHubUsername/Email:")
                    PrintResultat(e)
                    return False
            
            def main():
                
                if not LoggInnTilGitHub():
                    return False
                
                if not SettGitBrukernavnOgEmail():
                    return False
                
                else:
                    return True
            
            if not main():
                return False
            
            else:
                PrintStepSuccess("Authentication successful ...")
                return True
        
        def Init():  
                      
            def BoolErRepo(Directory):
                git_dir = os.path.join(Directory, '.git')
                if os.path.isdir(git_dir):
                    return True
                return False
            
            Dir = os.path.expanduser("~")
            Dir = Dir + "/" + RepoNavn
            # print("GitHub directory:", Dir); NL(0)
            
            os.chdir(Dir)
            CurrentWorkingDirectory = os.getcwd()
            
            PrintInfo("Current working directory:")
            PrintResultat(CurrentWorkingDirectory)
            
            if not BoolErRepo(Dir):
                command = f"git init {Dir}"
                Kommando(command)
                PrintSuccess("Directory initialized as a git repository ...")
                return True
            elif BoolErRepo(Dir):
                PrintSuccess("Directory is already a git repository, and will not be reinitialized ...")
                return True
            else :
                PrintError("Error initializing directory as a git repository ...")
                return False
         
        def Commit():
            PrintInfo("Attempting to commit changes ...")
            CommitMessage = "Script: Committing all changes "
            command = f"git commit -m '{CommitMessage}'"
            try:
                # Kommando(command)
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
                if "nothing to commit" in output:
                    PrintResultat(output)
                    PrintSuccess("No changes to commit ...")
                    return True
                else: 
                    print(output.encode())
                    PrintSuccess("Changes committed successfully ...")
                    return True
            except subprocess.CalledProcessError as e:
                if "Your branch is up to date" in e.output.decode():
                    PrintSuccess("Branch is up to date, no changes to commit ...")
                    return True
                if "Your branch is ahead of 'origin/main'" in e.output.decode():
                    PrintSuccess("Branch is ahead of origin branch message received, false error detected ...")
                    return True
                else:
                    resultat = e.output.decode()
                    if "nothing to commit" in resultat:
                        PrintSuccess("Ingen endringer trenger commit ...")
                        return True
                    PrintError("Error committing changes:")
                    PrintResultat(resultat)
                    return False

        def Branch():
            
            PrintInfo("Navigating to main branch ...")
            command = "git branch -M main"
            try:
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                PrintSuccess("On correct branch, main ...")
                return True
            except subprocess.CalledProcessError as e:
                if "fatal: A branch named 'main' already exists." in e.output.decode():
                    PrintSuccess("Main branch already exists, switching to branch ...")
                    branch_name = "main"
                    command = f"git checkout {branch_name}"
                    try:
                        Kommando(command)
                        return True
                    except subprocess.CalledProcessError as e:
                        PrintError("Error switching to main branch:", e.output.decode())
                        return False
                else:
                    PrintError("Error creating main branch:", e.output.decode())
                    return False
             
        def AddRemoteOrigin():
            
            def GitTestRemoteTilkoblinger():
            
                PrintDebug("Tester GitHub REMOTE tilkoblinger ...")
                
                Dir = os.path.expanduser("~")
                Dir = Dir + "/" + RepoNavn
                
                CurrentWorkingDirectory = os.getcwd()
                if CurrentWorkingDirectory != Dir:
                    CurrentWorkingDirectory = Dir
                    os.chdir(Dir)
                
                # print("Current working directory:", CurrentWorkingDirectory); NL(0)
                
                
                def test():
                
                    # Test
                    PrintInfo("TEST 1: Sjekker om det er satt opp remote koblinger med git remote kommando ...")
                    global remotes_output
                    remotes_output = None
                    
                    try:
                        
                        remotes_output = subprocess.check_output(["git", 
                                                                  "remote", 
                                                                  "-v"],
                                                                 stderr=subprocess.STDOUT).decode('utf-8')
                        
                        if "origin" and "None" in remotes_output:
                            PrintError("No remotes found...")
                            return False
                        
                        if remotes_output != None:
                    
                            PrintSuccess("List of all remotes:")
                            PrintResultat(remotes_output)
                        
                            PrintInfo("TEST 2: Sjekker om det er satt opp en 'origin' remote ...")
                            if 'origin' and "None" in remotes_output:
                                PrintError("No 'origin' remote found.")
                                return False
                            else :
                                PrintSuccess("Found 'origin' remote(s):")
                                for line in remotes_output.split("\n"):
                                    if 'origin' in line:
                                        PrintResultat(line.replace('origin', ''))
                                NL(0)
                                return remotes_output    
                                        
                        else:
                            PrintError("Ingen remotes ble funnet ..."); NL(2)
                        return False
                    except subprocess.CalledProcessError as e:
                        if "fatal: not a git repository" in str(e.output.decode()):
                            PrintError("Current directory is not a git repository ..."); NL(2)
                            return False
                        else:
                            PrintError("Git remote command failed ...")
                            return False
            
            
                if not test():
                    PrintError("Git origin remote test failed ...")
                    return False
                elif remotes_output:
                    PrintDebug("Git origin remote tests successful ...")
                    return remotes_output
                    
            def getOriginURL():       
                
                URLs = []
                
                PrintInfo("Attempting to retrieve remote URL using git ...")
                if GitTestRemoteTilkoblinger() == remotes_output:     
                    for line in remotes_output.split("\n"):
                        if 'origin' in line:
                            line = line.replace('origin', '')
                            line = line.replace('(push)', '')
                            line = line.replace('(fetch)', '')
                            URLs.append(line)
                            # print("Remote URL:", line)
                        if RepoNavn in URLs[0]:
                            PrintSuccess("Repo URL detected ...")
                            NL(0)
                            # PrintResultat(URLs[0])
                            return URLs[0]
                        else :
                            PrintError("No Repo URL detected")
                            return
                else:
                    PrintError("TestRemoteTilkoblinger() function produces no meaningful output ...")
                    PrintError("Error retrieving origin URL with git method in getOriginURL() function ...")
                    PrintInfo("Setting remote origing with the GitHub API...")
                    
                    def HentGitHubRepos():
                            
                        # PrintInfo("Henter GitHub repositorier ...")
                        
                        result = subprocess.run(["gh", 
                                                "repo", 
                                                "list", 
                                                "--limit", 
                                                "100"],
                                                capture_output=True, text=True)
                        
                        if result.returncode != 0:
                            PrintError("Error listing repositories")
                            return False
                        else:
                            PrintInfo("Repositories:")
                            PrintResultat(result.stdout)
                            PrintStepSuccess("Repositories listed successfully ...")
                            global APIOutput
                            APIOutput = result.stdout

                            return APIOutput
                    
                    resultat = HentGitHubRepos()
                    
                    if resultat == False:
                        PrintError("Error fetching GitHub repositories ...")
                        return False
                    
                    else:
                        
                        URLString = "https://github.com/"
                        
                        for line in APIOutput.split("\n"):
                            if RepoNavn in line:
                                PrintSuccess("Repo URL detected ...")
                                URLString += line.split(RepoNavn)[0].strip()
                                URLString += RepoNavn + ".git"
                                PrintResultat(URLString)
                                return URLString
                    
                        return URLString
                
        
            URL = getOriginURL()
            if URL == False:
                PrintError("No URL detected to add to origin remote ...")
                return False
            command = f"git remote add origin {URL}"
            # PrintDebug("Command:")
            # PrintResultat(command)
            PrintInfo("Attempting to add remote origin ...")
            
            try:
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                PrintSuccess("Remote origin added ...")
                return True
            except subprocess.CalledProcessError as e:
                if "error: remote origin already exists." in e.output.decode():
                    # PrintDebug(e.output.decode())
                    # PrintDebug(str(os.getcwd()))
                    PrintInfo("Origin for repository already exists ...")
                    command = f"git remote set-url origin {URL}"
                    try:
                        subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                        PrintSuccess("Remote origin set to URL ...")
                        return True
                    except subprocess.CalledProcessError as e:
                        PrintError("Error setting remote origin to URL:")
                        PrintResultat(e.output.decode())
                        return False
                else:
                    PrintError("Error adding remote origin and remote origin does not exist:")
                    PrintResultat(e.output.decode())
                    return False
       
        def PushOrigin():
                
                PrintInfo("Pushing changes to remote repository ...")
                command1 = "git push -u origin main"
                try:
                    if not Kommando(command1):
                        return False
                    PrintSuccess("Push successful ...")
                    return True
                except subprocess.CalledProcessError as e:
                    resultat = e.output.decode()
                    if "(fetch first)" in resultat:
                        command2 = "git pull origin main"
                        Kommando(command2)
                        Kommando(command1)
                        return True
                    PrintError("Error pushing to remote repository:")
                    PrintResultat(resultat)
                    return False
       
        def Pull():
            PrintInfo("Pulling changes from remote repository ...")
            command = "git pull origin main"
            try:
                if not Kommando(command):
                    return False
                PrintSuccess("Pull successful ...")
                return True
            except subprocess.CalledProcessError as e:
                PrintError("Error pulling from remote repository:")
                PrintResultat(e.output.decode())
                return False
        
        def main():
            
            if not Autentiser():
                PrintStepError("Error authenticating ...")
                return False
            
            elif not Init():
                PrintStepError("Error initializing directory as a git repository ...")
                return False

            elif not Commit():
                PrintStepError("Error committing changes ...")
                return False
            
            elif not Branch():
                PrintStepError("Error creating or switching to main branch ...")
                return False
            
            elif not AddRemoteOrigin():
                PrintStepError("Error adding remote origin ...")
                return False
            
            elif not Pull():
                PrintStepError("Error pulling from remote repository ...")
                return False
            
            elif not PushOrigin():
                PrintStepError("Error pushing to remote repository ...")
                return False
            
            else:
                return True
            
        if not main():
            return False
        else:
            PrintStepSuccess("SetupGit() function completed successfully ...")
            return True
    
    def main():
        
        TempKatalog = "/tmp"
        
        # email = "andreassalvesen1@outlook.com"
        
        ssh_key_path = HemmeligFilSti.replace(" ", "\ ") + "/id_rsa"
        print(ssh_key_path)
        # exit()
        if not SjekkMinnepinne():
            PrintStepError("USB-C minnepinne ikke tilkoblet. Avslutter ...")
            fjernSSHKeyFraAgent(HemmeligFilSti)
            return False
            
        if not SetupSSH(ssh_key_path, TempKatalog):
            PrintStepError("Error setting up SSH ...")
            return False
            
        if not SetupGit():
            PrintStepError("Error setting up Git ...")
            return False
        
        else: 
            return True
        
    if not main():
        PrintMainError("SetupGitOgPull() function failed ...")
        return False 
    else:
        PrintMainSuccess("SetupGitOgPull() function completed successfully ...")
        return True   

def SyncRepoTilGithub():
    
    # def HentGitHubRepos():
        
    #     PrintInfo("Henter GitHub repositorier ...")
        
    #     result = subprocess.run(["gh", 
    #                              "repo", 
    #                              "list", 
    #                              "--limit", 
    #                              "100"],
    #                             capture_output=True, text=True)
        
    #     if result.returncode != 0:
    #         PrintError("Error listing repositories")
    #         return False
    #     else:
    #         PrintInfo("Repositories:")
    #         PrintResultat(result.stdout)
    #         PrintStepSuccess("Repositories listed successfully ...")
    #         return True
        
    def CommitOgPushLokalRepo(): 
          
        def Add():

            PrintInfo("Attempting to add all files to staging area ...")
            command = "git add ."
            try:
                Kommando(command)
                PrintSuccess("All files added to staging area ...")
                return True
            except subprocess.CalledProcessError as e:
                PrintError("Error adding files to staging area:", e.output.decode())
                return False
            
        def Commit():
            PrintInfo("Attempting to commit changes ...")
            CommitMessage = "Script: Committing all changes "
            command = f"git commit -m '{CommitMessage}'"
            try:
                # Kommando(command)
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
                if "nothing to commit" in output:
                    PrintResultat(output)
                    PrintSuccess("No changes to commit ...")
                    return True
                else: 
                    print(output.encode())
                    PrintSuccess("Changes committed successfully ...")
                    return True
            except subprocess.CalledProcessError as e:
                if "Your branch is up to date" in e.output.decode():
                    PrintSuccess("Branch is up to date, no changes to commit ...")
                    return True
                if "Your branch is ahead of 'origin/main'" in e.output.decode():
                    PrintSuccess("Branch is ahead of origin branch message received, false error detected ...")
                    return True
                else:
                    PrintError("Error committing changes:")
                    PrintResultat(e.output.decode())
                    return False
            
        def Push():
            PrintInfo("Attempting to push changes to remote repository ...")
            command = "git push -u origin main"
            try:
                # Kommando(command)
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
                PrintResultat(output)
                
                if "Everything up-to-date" in output:
                    PrintSuccess("No changes to push ...")
                    return True
                else:
                    PrintSuccess("Changes pushed successfully ...")
                    return True
        
            except subprocess.CalledProcessError as e:
                PrintError("Error pushing changes:")
                PrintResultat(e.output.decode())
                return False
           
        def main():
            
            if not Add():
                PrintStepError("Error adding files to staging area ...")
                return False
            
            elif not Commit():
                PrintStepError("Error committing files ...")
                return False
            
            elif not Push():
                PrintStepError("Error pushing to remote repository ...")
                return False
            
            else: 
                return True
    
    
        if not main():
            return False
        else :
            PrintStepSuccess("LagOgPushLokalRepo() function completed successfully ...")
            return True
        
    def main():
        
        # if not HentGitHubRepos():
        #     PrintMainError("Error fetching GitHub repositories ...")
        #     return False
    
        if not CommitOgPushLokalRepo():
            PrintMainError("Error creating and pushing local repository ...")
            return False
        
        else: 
            return True
    
    if not main():
        PrintMainError("SyncRepoTilGithub() function failed ...")
        return False
    else:
        PrintMainSuccess("SyncRepoTilGithub() function completed successfully ...")
        return True

def SetupEnvironment():
    
    def installRClone():
        """Install RClone if not already installed."""
        try:
            subprocess.run(["rclone", "--version"], check=True)
            PrintSuccess("RClone is already installed.")
        except FileNotFoundError:
            PrintError("RClone is not installed. Installing RClone...")
            PrintInfo("Set up RClone with user input ...")
            subprocess.run("curl https://rclone.org/install.sh | sudo bash", shell=True, check=True)
    
    def configureRClone():
        """Configure RClone with the provided remote name."""
        configPath = os.path.expanduser("~/.config/rclone/rclone.conf")
        if not os.path.exists(configPath):
            PrintError("RClone is not configured ...")
            PrintInfo("Running rclone config...")
            subprocess.run(["rclone", "config"], check=True)
        else:
            PrintSuccess("RClone is already configured.")

    def createLocalDirectories():
        PrintInfo("Creating local directories...")
        if not os.path.exists(localBaseFolder):
            os.makedirs(localBaseFolder)
            print(f"Created local base folder: {localBaseFolder}")
        else:
            print(f"Local base folder already exists: {localBaseFolder}")

        for courseCode in courseCodes:
            coursePath = os.path.join(localBaseFolder, courseCode)
            if not os.path.exists(coursePath):
                os.makedirs(coursePath)
                print(f"Created course folder: {coursePath}")
            else:
                print(f"Course folder already exists: {coursePath}")

    installRClone()
    configureRClone()
    createLocalDirectories()

def MoveFilesBasedOnCriteria():
    """
    Move files based on criteria to specific folders on OneDrive.
    """

    def getSubfolders(courseCode):
        """Get the list of subfolders for a given course code from OneDrive."""
        result = subprocess.run(
            ["rclone", "lsf", f"{rcloneRemoteName}:{remoteBaseFolder}/{courseCode}/"],

            captureOutput=True, text=True
        )
        subfolders = result.stdout.strip().split('\n')
        return [sf for sf in subfolders if sf]
    
    for fileName in os.listdir(localBaseFolder):
        filePath = os.path.join(localBaseFolder, fileName)
        
        if os.path.isfile(filePath):
            for courseCode in courseCodes:
                if courseCode in fileName:
                    subfolder = None
                    subfolderIndicator = None
                    
                    # Check for subfolder indication in the filename (e.g., /F/ or /I/)
                    match = re.search(r"/([FI])/", fileName)
                    if match:
                        subfolderIndicator = match.group(1)
                    
                    # Construct the remote path
                    if subfolderIndicator:
                        subfolderList = getSubfolders(courseCode)
                        subfolder = next((sf for sf in subfolderList if sf.startswith(subfolderIndicator)), None)
                    
                    if subfolder:
                        targetPath = f"{rcloneRemoteName}:{remoteBaseFolder}/{courseCode}/{subfolder}/"
                    else:
                        targetPath = f"{rcloneRemoteName}:{remoteBaseFolder}/{courseCode}/"
                    
                    print(f"Moving {fileName} to {targetPath}")
                    
                    # Move file locally to avoid conflict with other operations
                    localTargetFolder = os.path.join(localBaseFolder, courseCode)
                    if subfolder:
                        localTargetFolder = os.path.join(localTargetFolder, subfolder)
                    localTargetPath = os.path.join(localTargetFolder, fileName)
                    os.makedirs(os.path.dirname(localTargetPath), exist_ok=True)
                    os.rename(filePath, localTargetPath)
                    
                    # Sync the local folder with OneDrive
                    subprocess.run(["rclone", "move", localTargetPath, targetPath])
                    break




#PROGRAM
# -----------------------------------------------------------------------------------------------------------------------------------------------------
def main(RepoNavn):
    
    # 0. Setup environment
    SetupEnvironment()
    # exit(0)
    
    # 1. Setup og pull repo, før programmet starter
    # FIKS: RepoNavn må inn her som variabel og må legges i hele funksjonen.
    if not SetupOgSyncRepoFraGitHub():
        return False
    
    # 2. Overvåk endringer i hjemmekatalogen
    # FIKS: RepoNavn må inn her som variabel og må legges i hele funksjonen.
    def Monitor():
        PrintInfo("Watching for changes in local directory, until program is stopped ...")
        current = snapshot_dir(os.path.expanduser(Path))

        
        PrintDebug("Initial snapshot:")
        PrintResultat(str(initial))
        
        if initial == {}:
            print("Initial snapshot is empty")
            pass

        if check_for_changes(initial, current):
            if SjekkMinnepinne():
                
                # 2. Synkroniser alle filer fra GitHub til hjemmekatalogen
                if not SyncRepoTilGithub():            
                    initial = current
                    return True
                
        if not check_for_changes(initial, current):
                return True

        else:
            PrintMainError("Feil ved overvåking av endringer i hjemmekatalogen, program avsluttes ...")
            return False
            
    
    # Denne kjører uendelig, og sjekker om minnepinnen er tilkoblet. 
    # Avslutter programmet dersom minnepinnen ikke er tilkoblet.
    if not Monitor():
        return False


# 0. Initialiser globale funksjoner
InitialiserGlobaleFunksjoner(); NL(2)


def SyncAlleKurs():
    
    global initial
    global RepoNavn
    global Path
    
    for course in courseCodes:
        
        RepoNavn = course
        PrintDebug("Kjører med reponavn: "), 
        PrintResultat(RepoNavn);time.sleep(2)
        
        Path = "~/" + RepoNavn
        PrintInfo("Path variabel:")
        PrintResultat(str(Path))
        
        initial = snapshot_dir(os.path.expanduser(Path))
        PrintDebug("Definerer initial:")
        PrintResultat(str(initial))
        
        initialList.append(initial)
        
        if initial == {}:
            print("Initial snapshot is empty")
            pass
        
        if not main(RepoNavn):
            pass
            # exit(1)



indikator = 0
initialList = []
while True:

    PrintInfo("Watching for new changes in local directory, until program is stopped ..."); NL(3)        
    SyncAlleKurs()    
    indikator += 1

    
#1. Bruk RClone til å synkronisere hjemmekatalogen til OneDrive

#2. Dersom det er en endring i OneDrive, synkroniser til hjemmekatalogen