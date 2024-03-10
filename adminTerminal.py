# Admin Terminal Alpha v1.31
# Made by Ghosted
# Software is open source, you can edit and customize and modify it anyway you want.

import os
import random
import time
import sys
"import tkinter as tk" # If not added in next update, it will be removed
import traceback
"import secrets" # If not added in next update, it will be removed
import json
from os.path import exists
from pathlib import Path
from tkinter.messagebox import *

if os.name == "posix":
    py_command = "python3"
    cls_command = "clear"
    pause_command = "/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'"
elif os.name == "nt":
    py_command = "py"
    cls_command = "cls"
    pause_command = "pause"

try:
    debug = False
    errorShow = False
    instantInstall = False

    if __name__ == "__main__":
        if len(sys.argv) > 1:
            if sys.argv[1] == "-debug":
                showinfo("Admin Terminal", "Debug Mode Enabled")
                debug = True
##            elif sys.argv[1] == "-showError":
##                errorShow = True
            elif sys.argv[1] == "-instantInstall":
                instantInstall = True
            elif sys.argv[1] == "-":
                print("No Argument Provided")
                os.system(pause_command)
                exit()
            else:
                showerror("Admin Terminal", f"Invalid Argument: {sys.argv[1]}")
                print(f"Invalid Argument, {sys.argv}")
                exit()
        else:
            pass

    if debug == True:
        print("Program Started!")

    winPath = Path.cwd()

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

    # dependenciesExist:
    settingsFileExists = exists(f"{winPath}\\settings.json")

    #files
    settingsFile = f"{winPath}\\settings.json"

    os.system(cls_command)

    if not settingsFileExists:
        filePermission = askyesno("Admin Terminal - NO SETTINGS FILE!", "Settings file is not installed, would you like to install it?", icon="warning")
        if filePermission == False or None:
            exit()
        settings = """{
    "settings":[
        {
            "debugMode": false,
            "version": "Version Alpha 1.31",
            "showAdvancedLogo": true,
            "author": "Made by Ghosted Alex",
            "showInstructions": true
        }
    ]
}"""
        file = open(settingsFile, "w")
        data = json.loads(settings)
        file.close()

        with open(settingsFile, "w") as f:
            f.write(settings)
            f.close()
        pass
    else:
        pass
    
    # LaunchVars
    showInstructions = False

    with open(settingsFile, "r") as f:
        j_data = f.read()
        j_obj = json.loads(j_data)
        j_list = j_obj["settings"]
    
    for i in range(len(j_list)):
        if j_list[i]:
            if j_list[i].get("debugMode") == True:
                debug = True
            if j_list[i].get("showInstructions") == True:
                showInstructions = True

    version = j_list[i].get("version")
    author = j_list[i].get("author")

    #vars
    logo = """
             _           _         _______                  _             _ 
    /\      | |         (_)       |__   __|                (_)           | |
   /  \   __| |________  _ ____      | | ___ ____ ________  _ ____   ____| |
  / /\ \ / _  |  _   _ \| |  _ \     | |/ _ \  __|  _   _ \| |  _ \ / _  | |
 / ____ \ (_| | | | | | | | | | |    | |  __/ |  | | | | | | | | | | (_| | |
/_/    \_\____|_| |_| |_|_|_| |_|    |_|\___|_|  |_| |_| |_|_|_| |_|\____|_|
"""

    print("\n")

    logo_txt = f"{author} | {version}"

    error = "\n\n"

    #functions    
    def loading_bar(total):
        for i in range(total+1):
            time.sleep(random.random())
            print('\r[' + '-'*i + ' '*(total-i) + ']', end='')
    
    def terminal():
        global error
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        else:
            print("Welcome to the Admin Terminal")
        print(logo_txt)
        if debug == True:
            print("Debug Mode Enabled")
        if showInstructions == True:
            print("Type 'help', 'patch' or 'info' for more information")
        print(error)
        userInput = input(f">>> {text_decor.color.OKCYAN}")
        print(f"{text_decor.style.END}")
        if userInput == "info":
            info()
        elif userInput == "file":
            os.system(cls_command)
            print("Loading File Mode")
            loading_bar(3)
            fileMode()
        elif userInput == "patch":
            patch_notes()
        elif userInput == "help":
            help()
        elif userInput == "?":
            help()
        elif userInput == "":
            os.system(cls_command)
            error = f"{text_decor.color.FAIL}Command is Empty!\nPlease enter a valid command{text_decor.style.END}\n"
            terminal()
        else:
            os.system(cls_command)
            error = f"{text_decor.color.FAIL}Unknown Command: {userInput}\nPlease check if the command exists{text_decor.style.END}\n"
            terminal()

    def help():
        os.system(cls_command)
        print('''Welcome to the Admin Terminal Help
This page is experimental so this page is subject to change, new commands will get added here when added
Available Commands:
    info - Shows info about the Admin Terminal
    file - Enables File Mode, needed for tasks with files/folders
    patch - Shows the patch notes
    help - Shows this page
    ? - Shows this page

File Mode Commands:
    create - Creates files/folders in a specified directory
    exit - Exits File Mode

If in File Mode, you can restart the Terminal to exit File Mode''')
        os.system(pause_command)
        os.system(cls_command)
        terminal()

    def patch_notes():
        os.system(cls_command)
        print(f'''{version}
Patch Notes:
-   Modified GUI [Graphical User Interface]
-   Changed Text in Info Page''')
        os.system(pause_command)
        os.system(cls_command)
        terminal()

    def info():
        os.system(cls_command)
        print(f'''{version}
Made by Ghosted Alex
Software is open source, you can edit and customize and modify it anyway you want.
The other python files in {winPath} are all of the dependencies for the Admin Terminal
Check out the github at https://github.com/Gh053d413x/Admin_Terminal''')
        os.system(pause_command)
        os.system(cls_command)
        terminal()

    def fileMode():
        os.system(cls_command)
        try:
            pathInput = input(f"{logo}\nFile Mode\nEnter a file path or type 'exit' to exit\n>>> ")
            if pathInput == "exit":
                os.system(cls_command)
                print("Exiting File Mode")
                loading_bar(3)
                os.system(cls_command)
                terminal()
            elif pathInput != "":
                os.system(cls_command)
                choice0 = input(f"{logo}\nFile Mode\nTo exit type 'exit'\nPath: {pathInput}\nAvailable Choices:\n- create\n- exit\n>>> ")
                if choice0 == "exit":
                    os.system(cls_command)
                    print("Exiting File Mode")
                    loading_bar(3)
                    os.system(cls_command)
                    terminal()
                elif choice0 == "create":
                    os.system(cls_command)
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
                        os.system(cls_command)
                        print(f"{choice1} is not a valid choice")
                        os.system(pause_command)
                        fileMode()
                else:
                    os.system(cls_command)
                    print(f"{choice0} is not a valid choice")
                    os.system(pause_command)
                    fileMode()
            elif pathInput == "":
                os.system(cls_command)
                print("Folder/File path can not be empty")
                os.system(pause_command)
                fileMode()
        except Exception as err:
            os.system(cls_command)
            print(f"An Error Occurred! Error: {err}")
            os.system(pause_command)
            fileMode()
    terminal()
except Exception as err:
    print(f"{text_decor.style.END}")
    os.system(cls_command)
    lineNum = traceback.format_exc()
    if debug == True:
        showerror("Admin Terminal", f"Admin Terminal has been terminated due to an exception\nError: {err}\n\nFull Error: {lineNum}")
        print(f"Admin Terminal has been terminated due to an exception\nError: {err}\n\nFull Error: {lineNum}")
    else:
        showerror("Admin Terminal", f"Admin Terminal has been terminated due to an exception\nError: {err}")
        print(f"Admin Terminal has been terminated due to an exception\nError: {err}\n\nFull Error: {lineNum}")
except KeyboardInterrupt:
    print(text_decor.style.END)
    quit()