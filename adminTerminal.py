import os
import random
import time
import sys
from os.path import exists
from pathlib import Path
from tkinter import messagebox as msg
import traceback
import secrets

try:
    debug = False
    errorShow = False

    if __name__ == "__main__":
        if len(sys.argv) > 1:
            if sys.argv[1] == "-debug":
                debug = True
            elif sys.argv[1] == "-showError":
                errorShow = True
            else:
                print("Invalid Argument")
        else:
            print("No Argument Provided")

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
        resourceFolderExists = exists(f"{winPath}/text_decor")
        aboutFileExists = exists(f"{winPath}/info.py")
        createFileExists = exists(f"{winPath}/create.py")

    #files
    info_file = f"{winPath}/info.py"
    create_file = f"{winPath}/create.py"

    temp = f"{winPath}/tmp_{encodedName}"
    encodedCode = secrets.token_urlsafe(512)

    os.system("cls")
    def loading_bar(total):
        for i in range(total+1):
            time.sleep(random.random())
            print('\r[' + '-'*i + ' '*(total-i) + ']', end='')
    def terminal():
        if errorShow == True:
            userInput = input(f"{text_decor.color.FAIL}Invalid Input has been entered\n{text_decor.style.END}>>> {text_decor.color.OKCYAN}")
        else:
            userInput = input(f">>> {text_decor.color.OKCYAN}")
        if userInput == "about":
            os.system(f"py {info_file}")
        elif userInput == "create":
            os.system(f"py {create_file}")
        else:
            print(f"{text_decor.color.FAIL}Invalid Command: {userInput} has ether a misspell or improper syntax{text_decor.style.END}")
            terminal()
    def createDependencies():
        t = open(temp, "w")
        t.write(encodedCode)
        print(f"Downloading and Copying files listed in {temp}. . .")
        loading_bar(15)
        os.system("cls")
        about = open(info_file, "w")
        about.write("""try:
    import os
    os.system('cls')
    print('''Admin Terminal\nVersion: 1.0\nAdmin Terminal is a terminal for admins\nPlease restart the Admin Terminal to continue''')
    os.system('pause')
    os.system('py ./adminTerminal.py')
except:
    os.system("./adminTerminal")""")
        about.close()

        print("Installing files. . .")
        loading_bar(15)

        crt = open(create_file, "w")
        crt.write("""try:
    import os
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
        os.system("py ./adminTerminal -errorShow")

    os.system("py ./adminTerminal")
except:
    os.system("py ./adminTerminal")""")
        crt.close()
        os.system("cls")
        print("Cleaning Up. . .")
        loading_bar(20)
        os.system("cls")
        t.close()
        os.remove(temp)
        if debug == True:
            print("Terminal Activated!")
        terminal()
    if dependenciesExist.aboutFileExists and dependenciesExist.createFileExists:
        if debug == True:
            print("Terminal Activated!")
        terminal()
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
    lineNum = traceback.format_exc()
    if debug == True:
        print(f"{text_decor.color.FAIL}Admin Terminal has been terminated due to an exception\nError: {err}\n\nFull Error: {lineNum}{text_decor.style.END}")
    else:
        print(f"{text_decor.color.FAIL}Admin Terminal has been terminated from an unknown crash{text_decor.style.END}")
except KeyboardInterrupt:
    print(f"{text_decor.color.FAIL}Admin Terminal has been terminated from a keyboard interruption{text_decor.style.END}")