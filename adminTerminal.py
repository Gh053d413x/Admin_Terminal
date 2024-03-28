# Admin Terminal Alpha 1.4
# Made by Ghosted
# Software is open source, you can edit and customize and modify it anyway you want.
try:
    import os
    import random
    import time
    import sys
    import tkinter as tk
    import traceback
    import json
    from time import sleep
    from os.path import exists
    from pathlib import Path
    from tkinter.messagebox import *
    
    if os.name == "posix":
        py_command = "python3"
        clear_command = "clear"
        pause_command = "/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'"
        remove_command = 'rm'
    elif os.name == "nt":
        py_command = "py"
        clear_command = "cls"
        pause_command = "pause"
        remove_command = "del"

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

    #functions    
    def loading_bar(total):
        for i in range(total+1):
            time.sleep(random.random())
            print('\r[' + '-'*i + ' '*(total-i) + ']', end='')

    os.system(clear_command)

    if not settingsFileExists:
        filePermission = askyesno("Admin Terminal - NO SETTINGS FILE!", "Settings file is not installed, would you like to install it?", icon="warning")
        if filePermission == False or None:
            exit()
        settings = """{
    "settings":[
        {
            "debugMode": false,
            "version": "Alpha 1.4",
            "showAdvancedLogo": true,
            "author": "Made by Ghosted Alex",
            "showInstructions": true,
            "password":""
        }
    ]
}"""
        file = open(settingsFile, "w+")
        file.write(settings)
        print("Waiting for Settings file download. . .")
        loading_bar(3)
        os.system(clear_command)
    else:
        os.system(clear_command)
    
    # LaunchVars
    showInstructions = False

    file = open(settingsFile, "r")

    j_data = file.read()
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
                os.system(clear_command)
                print("You are signed in!\nPlease Wait, the terminal is loading!")
                loading_bar(5)
                os.system(clear_command)
                terminal()
            else:
                os.system(clear_command)
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
        if debug == True:
            print("Debug Mode Enabled")
        if showInstructions == True:
            print("Type 'help', 'patch' or 'info' for more information\nType 'settings' to set settings")
        print(error)
        userInput = input(f">>> {text_decor.color.OKCYAN}")
        print(f"{text_decor.style.END}")
        if userInput == "info":
            info()
        elif userInput == "file":
            os.system(clear_command)
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
        elif userInput == "":
            os.system(clear_command)
            error = f"{text_decor.color.FAIL}Command is Empty!\nPlease enter a valid command{text_decor.style.END}\n"
            terminal()
        else:
            os.system(clear_command)
            error = f"{text_decor.color.FAIL}Unknown Command: {userInput}\nPlease check if the command exists{text_decor.style.END}\n"
            terminal()

    def setting():
        os.system(clear_command)
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        usrinput = input("Welcome to the Admin Terminal Settings\nAvailable Options:\n- set-password\n- reset\n>>> ")
        os.system(clear_command)
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
            os.system(clear_command)
            print("Password Set!")
            sleep(3)
            terminal()
        elif usrinput == "reset":
            user_input = askyesno("Admin Terminal - Settings Reset", "Are you sure you want to reset ALL settings?\nThis action can not be undone.", icon="warning")
            if user_input == True:
                os.system(f"{remove_command} ./settings.json")
                settings = """{
    "settings":[
        {
            "debugMode": false,
            "version": "Alpha 1.4",
            "showAdvancedLogo": true,
            "author": "Made by Ghosted Alex",
            "showInstructions": true,
            "password":""
        }
    ]
}"""
                file = open(settingsFile, "w+")
                file.write(settings)
                print("Waiting for Settings file download. . .")
                loading_bar(3)
                os.system(clear_command)
                print("Settings file has been reset!")
                os.system(pause_command)
                os.system(clear_command)
                terminal()
            else:
                setting()
        else:
            terminal()

    def assist():
        os.system(clear_command)
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

File Mode Commands:
    create - Creates files/folders in a specified directory
    exit - Exits File Mode

If in File Mode, you can restart the Terminal to exit File Mode''')
        os.system(pause_command)
        os.system(clear_command)
        terminal()

    def patch_notes():
        os.system(clear_command)
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        print(f'''{version}
Patch Notes (The Security Settings Update):
- Added a password system
- Added settings menu (type "settings" in the terminal to access them), you can still modify the settings via the settings file
- Added new commands to the Help Page
- Modified the Admin Terminal Logo

You can now reset the settings file!

You can also change the password as you wish

More settings will be added soon''')
        os.system(pause_command)
        os.system(clear_command)
        terminal()

    def info():
        os.system(clear_command)
        if j_list[i].get("showAdvancedLogo") == True:
            print(logo)
        print(f'''{logo_txt}
Software is open source, you can edit and customize and modify it anyway you want.
Check out the github at https://github.com/Gh053d413x/Admin_Terminal''')
        os.system(pause_command)
        os.system(clear_command)
        terminal()

    def fileMode():
        os.system(clear_command)
        try:
            pathInput = input(f"{logo}\nFile Mode\nEnter a file path or type 'exit' to exit\n>>> ")
            if pathInput == "exit":
                os.system(clear_command)
                print("Exiting File Mode")
                loading_bar(3)
                os.system(clear_command)
                terminal()
            elif pathInput != "":
                os.system(clear_command)
                choice0 = input(f"{logo}\nFile Mode\nTo exit type 'exit'\nPath: {pathInput}\nAvailable Choices:\n- create\n- exit\n>>> ")
                if choice0 == "exit":
                    os.system(clear_command)
                    print("Exiting File Mode")
                    loading_bar(3)
                    os.system(clear_command)
                    terminal()
                elif choice0 == "create":
                    os.system(clear_command)
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
                        os.system(clear_command)
                        print(f"{choice1} is not a valid choice")
                        os.system(pause_command)
                        fileMode()
                else:
                    os.system(clear_command)
                    print(f"{choice0} is not a valid choice")
                    os.system(pause_command)
                    fileMode()
            elif pathInput == "":
                os.system(clear_command)
                print("Folder/File path can not be empty")
                os.system(pause_command)
                fileMode()
        except Exception as err:
            os.system(clear_command)
            print(f"An Error Occurred! Error: {err}")
            os.system(pause_command)
            fileMode()
    logIn()
except Exception as err:
    print(f"{text_decor.style.END}")
    os.system(clear_command)
    lineNum = traceback.format_exc()
    showerror("Admin Terminal", f"Admin Terminal has been terminated due to an exception or an essential module is not installed\nError: {err}\n\nFull Error: {lineNum}")
    print(f"Admin Terminal has been terminated due to an exception or an essential module is not installed\nError: {err}\n\nFull Error: {lineNum}")    
except KeyboardInterrupt:
    print(text_decor.style.END)
    quit()