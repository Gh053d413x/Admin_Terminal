# Admin Terminal Alpha 1.7
# Almost to full release!
# Made by Ghosted
# Software is open source, you can edit and customize and modify it anyway you want.
# Log In Level Key: 0=User, 1=Moderator, 2=Admin

class text_decor:
    class color:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
    class style:
        END = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

settings = """{
    "settings":[
        {
            "devMode": false,
            "version": "Alpha 1.7",
            "showAdvancedLogo": true,
            "author": "Made by Ghosted Alex",
            "showInstructions": true,
            "maxLogInAttempts":3,
            "users":[
            
            ]
        }
    ]
}"""

try:
    import os
    import subprocess
    import random
    import time
    import sys
    import traceback
    import json
    from os.path import exists
    from pathlib import Path
    import shutil
    import datetime
    import getpass
    import hashlib
    try:
        import tkinter as tk
        import tkinter.ttk as ttk
        from tkinter import messagebox
        noGUI = None
    except ModuleNotFoundError:
        noGUI = True

    if os.name == "posix":
        py_command = "python3"
        clear_command = "clear"
        pause_command = "/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'"
        remove_command = 'rm'
        type_command = "cat"
    elif os.name == "nt":
        py_command = "py"
        clear_command = "cls"
        pause_command = "pause"
        remove_command = "del"
        type_command = "type"

    dev = False

    winPath = Path.cwd()

    # dependenciesExist:
    settingsFileExists = exists(f"{winPath}\\settings.json")

    # files
    settingsFile = f"{winPath}\\settings.json"

    # extra code

    # functions
    def loading_bar(total):
        subprocess.run(clear_command, shell=True)
        for i in range(total+1):
            time.sleep(random.uniform(0.1, 0.5))
            percent_complete = (i / total) * 100
            print('\r[' + '█'*i + '-'*(total-i) + f'] {percent_complete:.2f}%', end='')

    subprocess.run(clear_command, shell=True)

    if not settingsFileExists:
        if noGUI:
            filePermission = input("Admin Terminal - NO SETTINGS FILE!\nSettings file is not installed, would you like to install it? (y/n)\n>>> ")
            if filePermission == "n":
                exit()
            elif filePermission == "y" :
                subprocess.run(clear_command, shell=True)
            else:
                exit()
        else:
            filePermission = messagebox.askyesno("Admin Terminal - NO SETTINGS FILE!", "Settings file is not installed, would you like to install it?", icon="warning")
            if filePermission == False or None:
                exit()
        file = open(settingsFile, "w+")
        file.write(settings)
        print("Waiting for Settings file download. . .")
        loading_bar(10)
        subprocess.run(clear_command, shell=True)
    else:
        subprocess.run(clear_command, shell=True)
    
    # LaunchVars
    showInstructions = False

    file = open(settingsFile, "r")

    j_data = file.read()
    j_obj = json.loads(j_data)
    j_list = j_obj["settings"]

    for i in range(len(j_list)):
        if j_list[i]:
            if j_list[i].get("devMode") == True:
                dev = True
            if j_list[i].get("showInstructions") == True:
                showInstructions = True
    if j_list[i]["maxLogInAttempts"] >= 0:
        max_attempts = j_list[i].get("maxLogInAttempts")
    attempts = 0

    version = j_list[i].get("version")
    author = j_list[i].get("author")

    #vars
    logo = """  ___       _             _          _____                         _                _ 
 / _ \     | |           (_)        |_   _|                       (_)              | |
/ /_\ \  __| | ________   _  ____     | |    ___  ____  ________   _  ____    ____ | |
|  _  | / _  ||  _   _ \ | ||  _ \    | |   / _ \|  __||  _   _ \ | ||  _ \  / _  || |
| | | || (_| || | | | | || || | | |   | |  |  __/| |   | | | | | || || | | || (_| || |
\_| |_/ \__,_||_| |_| |_||_||_| |_|   \_/   \___||_|   |_| |_| |_||_||_| |_| \__,_||_|"""

    print("\n")

    logo_txt = f"{author} | {version}"

    checkSum = attempts * max_attempts / 2
    if checkSum != 0:
        startActions = True

    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    subprocess.run(clear_command, shell=True)

    error = "\n\n"
    def logIn():
        global attempts, max_attempts
        users = j_list[i].get("users", [])
        print(logo)
        if users:
            signInUser = input("Please enter your username:\n")
            signInPass = getpass.getpass("Please enter your password:\n")
            hashed_signInPass = hash_password(signInPass)  # Hash the input password
            user_found = False
            for user in users:
                if user["username"] == signInUser and user["password"] == hashed_signInPass:  # Compare hashed passwords
                    if not user["disabled"] == True:
                        user_found = True
                        subprocess.run(clear_command, shell=True)
                        terminal()
                        break
                    else:
                        subprocess.run(clear_command, shell=True)
                        print(f"{signInUser} is disabled!\nIf this was a mistake, please contact your administrator.")
                        logIn()
            if not user_found:
                attempts += 1
                subprocess.run(clear_command, shell=True)
                print(f"Username or password is incorrect!\nPlease try again. {attempts}/{max_attempts} Attempts Used\nUsername used: {signInUser}")
                if attempts != max_attempts:
                    logIn()
                else:
                    subprocess.run(clear_command, shell=True)
                    print(f"{attempts}/{max_attempts} Attempts Used, Please restart the terminal and try again")
                    subprocess.run(pause_command, shell=True)
                    sys.exit()
        else:
            username = input("There are currently no users, please enter a new username: ")
            password = input("Please enter a new password: ")
            createUser(username=username, password=password)

    def createUser(username, password):
        users = j_list[i].get("users", [])
        hashed_password = hash_password(password)  # Hash the password
        userDisabled = False
        new_user = {"username": username, "password": hashed_password, "disabled": userDisabled}
        users.append(new_user)
        j_list[i]["users"] = users
        with open(settingsFile, 'w') as file:
            json.dump(j_obj, file, indent=4)
        print("User added successfully.")
        subprocess.run(pause_command, shell=True)
        subprocess.run(clear_command, shell=True)
        logIn()

    def change_password(username, new_password):
        users = j_list[i].get("users", [])
        user_found = False
        for user in users:
            if user["username"] == username:
                user["password"] = new_password                
                user_found = True
                break
        if user_found:
            j_list[i]["users"] = users
            hashed_password = hash_password(new_password)  # Hash the password
            with open(settingsFile, 'w') as file:
                {"password": hashed_password}
            print("Password changed successfully.\nPlease restart the terminal to take effect")
            subprocess.run(pause_command, shell=True)
            sys.exit()
        else:
            print("User not found.")
            terminal()

    def terminal():
        global attempts
        attempts = 0
        file = open(settingsFile, "r")
        global error
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        else:
            print("Welcome to the Admin Terminal")
        print(logo_txt)
        if showInstructions == True:
            print("Type 'help', 'patch' or 'info' for more information\nType 'settings' to access the settings")
        print(error)
        userInput = input(f">>> {text_decor.color.OKCYAN}")
        print(f"{text_decor.style.END}")
        subprocess.run(clear_command, shell=True)
        if userInput == "info":
            info()
        elif userInput == "file":
            subprocess.run(clear_command, shell=True)
            print("Loading File Mode")
            loading_bar(5)
            fileMode()
        elif userInput == "patch":
            patch_notes()
        elif userInput == "help":
            assist()
        elif userInput == "?":
            assist()
        elif userInput == "assist":
            assist()
        elif userInput == "settings":
            setting()
        elif userInput == "backup":
            backup()
        elif userInput == "restore":
            restore()
        elif userInput == "":
            subprocess.run(clear_command, shell=True)
            error = f"{text_decor.color.FAIL}Command is Empty!\nPlease enter a valid command{text_decor.style.END}\n"
            terminal()
        else:
            subprocess.run(clear_command, shell=True)
            error = f"{text_decor.color.FAIL}Unknown Command: {userInput}\nPlease check if the command exists or you have permission to use it{text_decor.style.END}\n"
            terminal()

    def backup():
        subprocess.run(clear_command, shell=True)
        os.mkdir("backups")
        fileTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")[:-3]
        backupPath = f"{winPath}\\backups\\settings_backup_{fileTime}.json"
        settingsFileBackup = open(backupPath, "a")
        file = open(settingsFile, "r")
        for line in file:
            settingsFileBackup.write(line)
        print(f"Waiting for Settings Backup\nPath: {winPath}/backups/{backupPath}")
        loading_bar(10)
        subprocess.run(clear_command, shell=True)
        print("Settings have been Backed Up!\nPlease restart the terminal to take effect")
        subprocess.run(pause_command, shell=True)

    def restore():
        subprocess.run(clear_command, shell=True)
        backupPath = input("Where would you like to restore the settings file from?\n>>> ")
        shutil.copy(f"{winPath}\\backups\\{backupPath}", settingsFile)
        print(f"Waiting for Settings File Restore\nPath: {winPath}/backups/{backupPath}")
        loading_bar(10)
        subprocess.run(clear_command, shell=True)
        print("Settings have been Restored!\nPlease restart the terminal to take effect")
        subprocess.run(pause_command, shell=True)

    def setting():
        subprocess.run(clear_command, shell=True)
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        usrinput = input(f"Welcome to the Admin Terminal Settings\nAvailable Options:\n- set-login-attempts\n- change-password\n- reset-settings\n- show-settings\n- add-user\n\nLeave blank to go back to main menu\n>>> ")
        subprocess.run(clear_command, shell=True)

        if usrinput == "change-password":
            username = input("Enter a username: ")
            password = input("Enter a new password: ")
            change_password(username=username, new_password=password)

        elif usrinput == "set-login-attempts":
            global max_attempts
            file = open(settingsFile, "w")
            subprocess.run(clear_command, shell=True)
            if max_attempts != 0:
                print(f"Current Max Attempts: {max_attempts}")
            elif max_attempts == 0:
                print(f"Current Max Attempts: Disabled")
            editMaxAttempts = int(input("Enter attempts to modify\n>>> "))
            if editMaxAttempts == 0:
                j_list[i]["maxLogInAttempts"] = editMaxAttempts
                print("Max Attempts Disabled")
            elif editMaxAttempts > 0:
                j_list[i]["maxLogInAttempts"] = editMaxAttempts
                print(f"Max Attempts Set to {editMaxAttempts} attempts")
            elif editMaxAttempts < 0:
                print("Max Attempts can not be negative")
            else:
                print("Max Attempts was not able to be set")
            file = open(settingsFile, "w")
            subprocess.run(pause_command, shell=True)
            logIn()

        elif usrinput == "add-user":
            username = input("Enter a new username\n>>>")
            password = input("Enter a new password\n>>>")
            createUser(username=username, password=password)

        elif usrinput == "reset-settings":
            if noGUI:
                user_input = input("Admin Terminal - Settings Reset\nAre you sure you want to reset ALL settings?\nThis action can not be undone. (y/n)\n>>> ")
                if user_input == "y":
                    file = open(settingsFile, "w+")
                    file.write("")
                    print("Waiting for Settings File reset. . .")
                    loading_bar(10)
                    file.write(settings)
                    subprocess.run(clear_command, shell=True)
                    print("Waiting for Settings file reset. . .")
                    loading_bar(10)
                    subprocess.run(clear_command, shell=True)
                    print("Settings file has been reset!\n\nReset the terminal for changes to take effect")
                    subprocess.run(pause_command, shell=True)
                    subprocess.run(clear_command, shell=True)
                    sys.exit()
                else:
                    setting()
            else:
                user_input = messagebox.askyesno("Admin Terminal - Settings Reset", "Are you sure you want to reset ALL settings?\nThis action can not be undone.", icon="warning")
                if user_input == True:
                    file = open(settingsFile, "w+")
                    file.write("")
                    print("Waiting for Settings File reset. . .")
                    loading_bar(10)
                    file.write(settings)
                    subprocess.run(clear_command, shell=True)
                    print("Waiting for Settings file reset. . .")
                    loading_bar(10)
                    subprocess.run(clear_command, shell=True)
                    print("Settings file has been reset!\n\nReset the terminal for changes to take effect")
                    subprocess.run(pause_command, shell=True)
                    subprocess.run(clear_command, shell=True)
                    sys.exit()
                else:
                    setting()

        elif usrinput == "show-settings":
            subprocess.run(f"{type_command} settings.json", shell=True)
            print(j_list[i].get("settings"))
            subprocess.run(pause_command, shell=True)
            setting()
        elif usrinput == "adjust-logo":
            showLogo = j_list[i].get("showAdvancedLogo")
            print(logo)
        elif usrinput == "":
            terminal()
        else:
            setting()

    def assist():
        subprocess.run(clear_command, shell=True)
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        print('''Welcome to the Admin Terminal Help
This page is experimental so this page is subject to change, new commands will get added here when added
Available Commands:
    info - Shows info about the Admin Terminal
    file - Enables File Mode, needed for tasks with files/folders
    patch - Shows the patch notes
    help - Shows this page
    ? - Shows this page
    assist - Shows this page
    settings - Brings up settings menu
    backup - Backs Up the Settings File
    restore - Restores the Settings File Backup to the Settings File

File Mode Commands:
    create - Creates files/folders in a specified directory
    exit - Exits File Mode

Settings Menu:
    set-password - Sets the password
    reset-settings - Resets the settings file
    show-settings - Shows the raw json settings

If in File Mode, you can restart or type "exit" the Terminal to exit File Mode''')
        subprocess.run(pause_command, shell=True)
        subprocess.run(clear_command, shell=True)
        terminal()

    def patch_notes():
        subprocess.run(clear_command, shell=True)
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        print(f'''{version}
Patch Notes:
-   Replaced password system with user system
-   Passwords are now encrypted
-   Fixed bugs for python installations where essential modules are not present or for older versions of python (3.8.x and below)''')
        subprocess.run(pause_command, shell=True)
        subprocess.run(clear_command, shell=True)
        terminal()

    def info():
        subprocess.run(clear_command, shell=True)
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        print(f'''{logo_txt}
Software is open source, you can edit and customize and modify it anyway you want.
Check out the github at https://github.com/Gh053d413x/Admin_Terminal''')
        subprocess.run(pause_command, shell=True)
        subprocess.run(clear_command, shell=True)
        terminal()

    def fileMode():
        subprocess.run(clear_command, shell=True)
        try:
            pathInput = input(f"{logo}\nFile Mode\nEnter a file path or type 'exit' to exit\n>>> ")
            if pathInput == "exit":
                subprocess.run(clear_command, shell=True)
                print("Exiting File Mode")
                loading_bar(5)
                subprocess.run(clear_command, shell=True)
                terminal()
            elif pathInput != "":
                subprocess.run(clear_command, shell=True)
                choice0 = input(f"{logo}\nFile Mode\nTo exit type 'exit'\nPath: {pathInput}\nAvailable Choices:\n- create\n- exit\n>>> ")
                if choice0 == "exit":
                    subprocess.run(clear_command, shell=True)
                    print("Exiting File Mode")
                    loading_bar(5)
                    subprocess.run(clear_command, shell=True)
                    terminal()
                elif choice0 == "create":
                    subprocess.run(clear_command, shell=True)
                    choice1 = input(f"{logo}\nFile Mode\nPath: {pathInput}\nWhat do you want to do?\nAvailable Choices:\n- folder\n- file\n>>> ")
                    if choice1 == "file":
                        file = open(pathInput, "w")
                        file.close()
                        fileMode()
                    elif choice1 == "folder":
                        os.mkdir(pathInput)
                        fileMode()
                    elif choice1 == "-file":
                        file = open(pathInput, "w")
                        file.close()
                        fileMode()
                    elif choice1 == "-folder":
                        os.mkdir(pathInput)
                        fileMode()
                    if choice1 == "- file":
                        file = open(pathInput, "w")
                        file.close()
                        fileMode()
                    elif choice1 == "- folder":
                        os.mkdir(pathInput)
                        fileMode()
                    else:
                        subprocess.run(clear_command, shell=True)
                        print(f"{choice1} is not a valid choice")
                        subprocess.run(pause_command, shell=True)
                        fileMode()
                else:
                    subprocess.run(clear_command, shell=True)
                    print(f"{choice0} is not a valid choice")
                    subprocess.run(pause_command, shell=True)
                    fileMode()
            elif pathInput == "":
                subprocess.run(clear_command, shell=True)
                print("Folder/File path can not be empty")
                subprocess.run(pause_command, shell=True)
                fileMode()
        except Exception as err:
            subprocess.run(clear_command, shell=True)
            print(f"An Error Occurred! Error: {err}")
            subprocess.run(pause_command, shell=True)
            fileMode()
    logIn()
except Exception as err:
    print(f"{text_decor.style.END}")
    subprocess.run(clear_command, shell=True)
    lineNum = traceback.format_exc()
    try:
        messagebox.showerror("Admin Terminal", f"Admin Terminal has been terminated due to an exception or an essential module is not installed\nError: {err}\n\nFull Error: {lineNum}")
    except:
        print(f"Admin Terminal has been terminated due to an exception or an essential module is not installed\nError: {err}\n\nFull Error: {lineNum}")
        subprocess.run(pause_command, shell=True)
    sys.exit()
except KeyboardInterrupt:
    subprocess.run(clear_command, shell=True)
    print(text_decor.style.END)
    quit()