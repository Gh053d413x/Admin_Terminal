# Admin Terminal Alpha v1.1
# Made by Ghosted
# Software is free, you can edit and customize it 
# because it is Open Source!

import os
import random
import time
import sys
from os.path import exists
from pathlib import Path
from tkinter import messagebox as msg
import tkinter
import traceback
import secrets
from venv import logger

try:
    debug = False
    errorShow = False
    instantInstall = False

    if __name__ == "__main__":
        if len(sys.argv) > 1:
            if sys.argv[1] == "-debug":
                msg.showinfo("Admin Terminal", "Debug Mode Enabled")
                debug = True
            elif sys.argv[1] == "-showError":
                errorShow = True
            elif sys.argv[1] == "-instantInstall":
                instantInstall = True
            elif sys.argv[1] == "-":
                msg.showerror("Admin Terminal", "No Argument Provided")
                print("No Argument Provided")
                exit()
            else:
                msg.showerror("Admin Terminal", f"Invalid Argument: {sys.argv[1]}")
                print(f"Invalid Argument, {sys.argv}")
                exit()
        else:
            pass

    if debug == True:
        print("Program Started!")

    winPath = Path.cwd()
    encodedName = secrets.token_urlsafe(32)

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

    class dependenciesExist:
        "This is where all of the dependencies will exist"
        createFileExists = exists(f"{winPath}/create.py")

    logo = """
             _           _         _______                  _             _ 
    /\      | |         (_)       |__   __|                (_)           | |
   /  \   __| |________  _ ____      | | ___ ____ ________  _ ____   ____| |
  / /\ \ / _  |  _   _ \| |  _ \     | |/ _ \  __|  _   _ \| |  _ \ / _  | |
 / ____ \ (_| | | | | | | | | | |    | |  __/ |  | | | | | | | | | | (_| | |
/_/    \_\____|_| |_| |_|_|_| |_|    |_|\___|_|  |_| |_| |_|_|_| |_|\____|_|
Alpha"""

    #files
    info_file = f"{winPath}/info.py"
    create_file = f"{winPath}/create.py"

    temp = f"{winPath}/tmp_{encodedName}"
    encodedCode = secrets.token_urlsafe(512)

    os.system("cls")

    #functions
    
    def loading_bar(total):
        for i in range(total+1):
            time.sleep(random.random())
            print('\r[' + '-'*i + ' '*(total-i) + ']', end='')
    
    def terminal():
        print(logo)
        if errorShow == True:
            userInput = input(f"{text_decor.color.FAIL}Invalid Input has been entered\n{text_decor.style.END}>>> {text_decor.color.OKCYAN}")
        else:
            userInput = input(f">>> {text_decor.color.OKCYAN}")
            print(f"{text_decor.style.END}")
        if userInput == "info":
            info()
        elif userInput == "create":
            os.system(f"py {create_file}")
        else:
            os.system("cls")
            print(f"{text_decor.color.FAIL}Invalid Command: {userInput} has ether a misspell or improper syntax{text_decor.style.END}")
            terminal()

    def info():
        os.system('cls')
        print(f'''Admin Terminal v1.1
Made by Ghosted
Software is free, you can edit and customize it because it is Open Source!
The other python files in {winPath} are all of the dependencies for the Admin Terminal
Check out the github at https://github.com/Gh053d413x/Admin_Terminal''')
        os.system('pause')
        os.system("cls")
        terminal()

    def createDependencies():
        print(f"Downloading and Copying files listed in {temp}. . .")
        loading_bar(15)

        print("Installing files. . .")
        loading_bar(15)

        crt = open(create_file, "w")
        crt.write("""import os
try:
    from pathlib import Path
    os.system('cls')
    winPath = Path.cwd()
    userInput = input('''Enter the path you want the File/Folder to be in
    >>> ''')
    if userInput == "":
        os.system("py ./create.py")
    else:
        path = userInput
    os.system('cls')

    print("Path set to: " + path)
    fileFolder = input('''Which do you want to create?
    Available Options:
    * File
    * Folder
    >>> ''')
    if fileFolder == "file":
        file = open(path)
        file.close()
    elif fileFolder == "folder":
        os.mkdir(path)
    else:
        os.system("cls")
        os.system("py ./adminTerminal.py -errorShow")

    os.system("py ./adminTerminal.py")
except:
    os.system("py ./adminTerminal.py")""")
        crt.close()
        os.system("cls")
        print("Cleaning Up. . .")
        loading_bar(20)
        os.system("cls")
        if debug == True:
            print("Terminal Activated!")
        terminal()

    if dependenciesExist.createFileExists:
        if debug == True:
            print("Terminal Activated!")
        terminal()
    else:
        if instantInstall == True:
            if debug == True:
                print("Installing Dependencies")
            createDependencies()
        else:
            if debug == True:
                print("DEPENDENCIES MISSING!")
            installConfirm = msg.askyesno("Admin Terminal", "One or More dependencies are not installed\nWould you like to install the dependencies?", icon="error")
            if installConfirm == True:
                if debug == True:
                    print("Installing Dependencies")
                createDependencies()
            else:
                quit()
except Exception as err:
    print(f"{text_decor.style.END}")
    os.system("cls")
    lineNum = traceback.format_exc()
    if debug == True:
        msg.showerror("Admin Terminal", f"Admin Terminal has been terminated due to an exception\nError: {err}\n\nFull Error: {lineNum}")
    else:
        msg.showerror("Admin Terminal", "Admin Terminal has been terminated from an unknown crash")
except KeyboardInterrupt:
    print(f"{text_decor.style.END}")
    os.system("cls")
    msg.showerror("Admin Terminal", "Admin Terminal has been terminated from a keyboard interruption")