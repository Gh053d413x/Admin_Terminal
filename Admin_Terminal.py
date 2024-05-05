# Admin Terminal Alpha 1.5
# Made by Ghosted
# Software is open source, you can edit and customize and modify it anyway you want.

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

import tkinter as tk
from tkinter.messagebox import *

settings = """{
    "settings":[
        {
            "devMode": false,
            "version": "Alpha 1.5",
            "showAdvancedLogo": true,
            "author": "Made by Ghosted Alex",
            "showInstructions": true,
            "password":""
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
    from time import sleep
    from os.path import exists
    from pathlib import Path
    import shutil
    import datetime
    
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

    # functions    
    def loading_bar(total):
        for i in range(total+1):
            time.sleep(random.random())
            print('\r[' + '-'*i + ' '*(total-i) + ']', end='')

    subprocess.run(clear_command, shell=True)

    if not settingsFileExists:
        filePermission = askyesno("Admin Terminal - NO SETTINGS FILE!", "Settings file is not installed, would you like to install it?", icon="warning")
        if filePermission == False or None:
            exit()
        file = open(settingsFile, "w+")
        file.write(settings)
        print("Waiting for Settings file download. . .")
        loading_bar(3)
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

    error = "\n\n"
    def logIn():
        if j_list[i].get("password") != "":
            signIn = input("Please enter the Admin Terminal Password\n>>> ")
            if j_list[i].get("password") == signIn:
                subprocess.run(clear_command, shell=True)
                terminal()
            else:
                subprocess.run(clear_command, shell=True)
                print("Password is incorrect!\nPlease try again.")
                logIn()
        elif j_list[i].get("password") == "":
            terminal()

    def terminal():
        file = open(settingsFile, "r")
        global error
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        else:
            print("Welcome to the Admin Terminal")
        print(logo_txt)
        if showInstructions == True:
            if dev == True:
                print("Type 'help', 'patch' or 'info' for more information\nType 'settings' to access the settings\nType 'gui' to enter GUI\nType 'dev-settings' to access Dev Settings (Developers can add their own settings/commands with this menu)")
            else:
                print("Type 'help', 'patch' or 'info' for more information\nType 'settings' to access the settings\nType 'gui' to enter GUI")
        print(error)
        userInput = input(f">>> {text_decor.color.OKCYAN}")
        print(f"{text_decor.style.END}")
        if userInput == "info":
            info()
        elif userInput == "file":
            subprocess.run(clear_command, shell=True)
            print("Loading File Mode")
            loading_bar(3)
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
        elif userInput == "dev-settings":
            if dev == True:
                devSetting()
            else:
                subprocess.run(clear_command, shell=True)
                error = f"{text_decor.color.FAIL}Unknown Command: dev-settings\nPlease check if the command exists or you have permission to use it{text_decor.style.END}\n"
                terminal()
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
        loading_bar(3)
        subprocess.run(clear_command, shell=True)
        print("Settings have been Backed Up!\nPlease restart the terminal to take effect")
        subprocess.run(pause_command, shell=True)

    def restore():
        subprocess.run(clear_command, shell=True)
        backupPath = input("Where would you like to restore the settings file from?\n>>> ")
        shutil.copy(f"{winPath}\\backups\\{backupPath}", settingsFile)
        print(f"Waiting for Settings File Restore\nPath: {winPath}/backups/{backupPath}")
        loading_bar(3)
        subprocess.run(clear_command, shell=True)
        print("Settings have been Restored!\nPlease restart the terminal to take effect")
        subprocess.run(pause_command, shell=True)

    def devSetting():
        terminal()

    def setting():
        subprocess.run(clear_command, shell=True)
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        if j_list[i].get("password") == "":
            password = "No Password Set!"
        elif j_list[i].get("password") != "":
            password = j_list[i].get("password")
        usrinput = input(f"Password: {password}\nWelcome to the Admin Terminal Settings\nAvailable Options:\n- set-password\n- reset-settings\n- show-settings\n\nLeave blank to go back to main menu\n>>> ")
        subprocess.run(clear_command, shell=True)
        if usrinput == "set-password":
            passw = input("Enter a new password\nIf blank, the password won't be required to log in\n>>> ")
            file = open(settingsFile, "w")
            j_list[i]["password"] = passw
            try:
                # Writing to JSON file
                with open(settingsFile, "w") as file:
                    json.dump(j_obj, file, indent=4)
                    file.flush()  # Flush the buffer
            except Exception as e:
                print("Error:", e)
            file = open(settingsFile, "r")
            subprocess.run(clear_command, shell=True)
            print("Password Set!")
            sleep(3)
            terminal()
        elif usrinput == "reset-settings":
            user_input = askyesno("Admin Terminal - Settings Reset", "Are you sure you want to reset ALL settings?\nThis action can not be undone.", icon="warning")
            if user_input == True:
                file = open(settingsFile, "w+")
                file.write("")
                print("Waiting for Settings File reset. . .")
                loading_bar(3)
                file.write(settings)
                subprocess.run(clear_command, shell=True)
                print("Waiting for Settings file reset. . .")
                loading_bar(3)
                subprocess.run(clear_command, shell=True)
                print("Settings file has been reset!\n\nReset the terminal for changes to take effect")
                subprocess.run(pause_command, shell=True)
                subprocess.run(clear_command, shell=True)
                sys.exit()
            else:
                setting()
        elif usrinput == "show-settings":
            subprocess.run(f"{type_command} settings.json", shell=True)
            print()
            subprocess.run(pause_command, shell=True)
            setting()
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

If in File Mode, you can restart the Terminal to exit File Mode''')
        subprocess.run(pause_command, shell=True)
        subprocess.run(clear_command, shell=True)
        terminal()

    def patch_notes():
        subprocess.run(clear_command, shell=True)
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        print(f'''{version}
Patch Notes:
-   Added a Backup and Restore function for the Settings File''')
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
                loading_bar(3)
                subprocess.run(clear_command, shell=True)
                terminal()
            elif pathInput != "":
                subprocess.run(clear_command, shell=True)
                choice0 = input(f"{logo}\nFile Mode\nTo exit type 'exit'\nPath: {pathInput}\nAvailable Choices:\n- create\n- exit\n>>> ")
                if choice0 == "exit":
                    subprocess.run(clear_command, shell=True)
                    print("Exiting File Mode")
                    loading_bar(3)
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
    showerror("Admin Terminal", f"Admin Terminal has been terminated due to an exception or an essential module is not installed\nError: {err}\n\nFull Error: {lineNum}")
    print(f"Admin Terminal has been terminated due to an exception or an essential module is not installed\nError: {err}\n\nFull Error: {lineNum}")
    sys.exit()
except KeyboardInterrupt:
    subprocess.run(clear_command, shell=True)
    print(text_decor.style.END)
    quit()