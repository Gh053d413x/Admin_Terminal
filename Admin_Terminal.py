CUR_VER = "25w20a/Snapshot"
# Admin Terminal is a terminal program that allows you to run commands and manage files and folders
# Made by Ghosted Alex
# Software is free, you can edit and customize and modify it anyway you want.

# Patch Notes:
# + Added More Logo Options
# + Added Safe Guards for Incompatible Versions
# + Added a Crash Message when Admin Terminal Couldn't Even Enter the Early Stages of Starting Up
# + Added the "CUR_VER" Variable (Can be used Anywhere) - CUR_VER means Current Version
# + Added the Ability to Generate hex, bytes and urlsafe tokens with the secrets library - Can also be used to create UUIDs, IDs and Keys!
# + Added a CLI (Command Line Interface) Mode - Can be enabled in the settings.json file
# * Modified settings to change: show_instructions and max_log_in_attempts to instructions and max_attempts respectively
# + Added a WARNING file that warns users about the dangers of modding the terminal

# Be aware that any future code will go into the packages folder, either you can create your own packages or download packages from the packages branch

try:
    class text_decor:
        class color:
            HEADER = '\033[95m'
            OKBLUE = '\033[94m'
            OKCYAN = '\033[96m'
            OKGREEN = '\033[92m'
            WARNING = '\033[93m'
            FAIL = '\033[91m'
        class style:
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
        RESET = '\033[0m'

    import os
    from typing import NoReturn
    import subprocess
    import random
    import time
    import sys
    from sys import argv
    import traceback
    import json
    from os.path import exists, isdir
    from pathlib import Path
    import shutil
    import datetime
    from getpass import getpass
    import hashlib
    import secrets

    if os.name == "posix":
        PY_COMMAND = "python3"
        CLEAR_COMMAND = "clear"
        PAUSE_COMMAND = "/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'"
        REMOVE_COMMAND = 'sudo rm -rf'
        TYPE_COMMAND = "cat"
    elif os.name == "nt":
        PY_COMMAND = "py"
        CLEAR_COMMAND = "cls"
        PAUSE_COMMAND = "pause"
        REMOVE_COMMAND = "del"
        TYPE_COMMAND = "type"

    SETTINGS = """{
  "settings":[
    {
      "version": \"""" + CUR_VER + """\",
      "master_password": "",
      "logo": 2,
      "author": "Made by Ghosted Alex",
      "instructions": true,
      "max_attempts":3,
      "use_cli": false,
      "users":[

      ]
    }
  ]
}"""

    MODS = """{
        "mods":[

        ]
    }"""

    WARNING = """If you are modding the terminal,
you might want to be careful with what you are doing.

The terminal is delecate and if not handeled properly, it will brick the terminal.
Only proceed if you know what you are doing!

Beware of the developer's curse!"""

    inp = ""

    WINPATH = Path.cwd()

    with open(f"{WINPATH}/WARNING", "w") as warning:
        warning.write(WARNING)

    # dependenciesExist
    SETTINGS_FILE_EXISTS = exists(fr"{WINPATH}\settings.json")
    MODS_FILE_EXISTS = exists(fr"{WINPATH}\mods.json")
    CONFIG_FOLDER_EXISTS = isdir(fr"{WINPATH}\config")
    MODS_FOLDER_EXISTS = isdir(fr"{WINPATH}\mods")
    PACKAGE_FOLDER_EXISTS = isdir(fr"{WINPATH}\packages")

    # files
    SETTINGS_FILE = fr"{WINPATH}\settings.json"
    MODS_FILE = fr"{WINPATH}\mods.json"

    # folders
    MODS_FOLDER = fr"{WINPATH}\mods"
    CONFIG_FOLDER = fr"{WINPATH}\config"
    PACKAGE_FOLDER = fr"{WINPATH}\packages"
    
    EXPERIMENTAL = False

    users_list = []
    
    mod_data = []

    # logo
    logo = r"""      ___       _             _          _____                         _                _
     / _ \     | |           (_)        |_   _|                       (_)              | |
    / /_\ \  __| | ________   _  ____     | |    ___  ____  ________   _  ____    ____ | |
    |  _  | / _  ||  _   _ \ | ||  _ \    | |   / _ \|  __||  _   _ \ | ||  _ \  / _  || |
    | | | || (_| || | | | | || || | | |   | |  |  __/| |   | | | | | || || | | || (_| || |
    \_| |_/ \__,_||_| |_| |_||_||_| |_|   \_/   \___||_|   |_| |_| |_||_||_| |_| \__,_||_|"""
    
    # Load Settings
    try:
        import tkinter as tk
        import tkinter.ttk as ttk
        from tkinter import simpledialog
        from tkinter import messagebox
        import psutil
        no_user_interface = None
    except ModuleNotFoundError or ImportError as moduleErr:
        subprocess.run(CLEAR_COMMAND, shell=True)
        input(f"{logo}\nERROR\nThere was a problem loading specific modules: {moduleErr.name}\nIf Applicable, Please Install {moduleErr.name} using \"pip install {moduleErr.name}\"\nIf you continue, the admin terminal might not run properly!\nPress CTRL + C to quit or Press ENTER to continue")
        no_user_interface = True
    
    s_file = open(SETTINGS_FILE, "r")
    m_file = open(MODS_FILE, "r")

    j_data = s_file.read()
    j_obj = json.loads(j_data)
    j_list = j_obj["settings"]

    for i in range(len(j_list)):
        if j_list[i]:
            if j_list[i].get("instructions") == True:
                instructions = True

    if j_list[i]["max_attempts"] >= 0:
        max_attempts = j_list[i].get("max_attempts")
    else:
        if no_user_interface == False:
            messagebox.showerror("Admin Terminal Error", "The Maximum Attempts can not be lower than 0. Please set the number equal to or higher than 0\n0 - Disables Max Log In Attempts\n1 and above - Sets Log In Attempts to set number")
            sys.exit()
        else:
            print(f"{text_decor.color.FAIL}The Maximum Attempts can not be lower than 0. Please set the number equal to or higher than 0\n0 - Disables Max Log In Attempts\n1 and above - Sets Log In Attempts to set number{text_decor.RESET}")

    # functions
    def load_mods() -> list:
        if MODS_FILE_EXISTS:
            with open(MODS_FILE, "r") as m_file:
                mod_data = json.load(m_file)
                return mod_data.get("mods", [])
        else:
            return []
    
    def load_process(total, reason):
        subprocess.run(CLEAR_COMMAND, shell=True)
        if reason != "":
            print(reason)
        else:
            print("")
        for i in range(total+1):
            time.sleep(random.uniform(0.1, 0.5))
            percent_complete = (i / total) * 100
            print(f'\r[' + '#'*i + '='*(total-i) + f'] {percent_complete:.2f}%', end='')

    try:
        if no_user_interface == None:
            if j_list[i].get("use_cli") == True:
                no_user_interface = True

        subprocess.run(CLEAR_COMMAND, shell=True)

        if not SETTINGS_FILE_EXISTS or not PACKAGE_FOLDER_EXISTS:
            if no_user_interface:
                match input(f"Admin Terminal - NO ESSENTIAL FILES!\n1 or More Essential Files/folders are not installed, would you like to install them? [Will be installed in {WINPATH}]\n(y/n)\n>>> "):
                    case "n":
                        subprocess.run(CLEAR_COMMAND, shell=True)
                        print("Unable to install essential files due to user cancellation\nPlease try again later")
                        subprocess.run(PAUSE_COMMAND, shell=True)
                        sys.exit()
                    case "y":
                        subprocess.run(CLEAR_COMMAND, shell=True)
                    case _:
                        sys.exit()
            else:
                match messagebox.askyesno("Admin Terminal - NO ESSENTIAL FILES!", f"1 or More Essential Files are not installed, would you like to install them?\n(Will be installed in {WINPATH})", icon="warning"):
                    case False:
                        messagebox.showerror("Admin Terminal - Error", "Unable to install essential files due to user cancellation\nPlease try again later")
                        sys.exit()
                    case None:
                        messagebox.showerror("Admin Terminal - Error", "Unable to install essential files due to user cancellation\nPlease try again later")
                        sys.exit()
                    case _:
                        if not SETTINGS_FILE_EXISTS:
                            with open(SETTINGS_FILE, "w+") as s_file:
                                load_process(10, "Creating Settings File...")
                                s_file.write(SETTINGS)
                                subprocess.run(CLEAR_COMMAND, shell=True)
                        try:
                            if not PACKAGE_FOLDER_EXISTS:
                                load_process(10, "Creating Packages Folder...")
                                os.mkdir(PACKAGE_FOLDER)    
                        except:
                            ...
        else:
            subprocess.run(CLEAR_COMMAND, shell=True)

        # LaunchVars
        instructions = False

        logged_in = False

        attempts = 0
        
        logged_in = False
        
        debug = False

        version = j_list[i].get("version")
        author = j_list[i].get("author")

        if version != "01y25w01a/Snapshot":
            if no_user_interface == True:
                print(f"{text_decor.color.WARNING}WARNING: The current version {version} is currently out of date! The admin Terminal will not work properly at all without the latest version!")
                print(f"{text_decor.color.WARNING}WARNING: The current version {version} is currently out of date! The admin Terminal will not work properly at all without the latest version!")

        #vars
        match j_list[i]["logo"]:
            case 0:
                logo = ""
            case 1:
                logo = r"""                 _           _         _______                  _             _
        /\      | |         (_)       |__   __|                (_)           | |
       /  \   __| |________  _ ____      | | ___ ____ ________  _ ____   ____| |
      / /\ \ / _  |  _   _ \| |  _ \     | |/ _ \  __|  _   _ \| |  _ \ / _  | |
     / ____ \ (_| | | | | | | | | | |    | |  __/ |  | | | | | | | | | | (_| | |
    /_/    \_\____|_| |_| |_|_|_| |_|    |_|\___|_|  |_| |_| |_|_|_| |_|\____|_|"""
            case 2:
                logo = r"""      ___       _             _          _____                         _                _
     / _ \     | |           (_)        |_   _|                       (_)              | |
    / /_\ \  __| | ________   _  ____     | |    ___  ____  ________   _  ____    ____ | |
    |  _  | / _  ||  _   _ \ | ||  _ \    | |   / _ \|  __||  _   _ \ | ||  _ \  / _  || |
    | | | || (_| || | | | | || || | | |   | |  |  __/| |   | | | | | || || | | || (_| || |
    \_| |_/ \__,_||_| |_| |_||_||_| |_|   \_/   \___||_|   |_| |_| |_||_||_| |_| \__,_||_|"""

        print("\n")

        if j_list[i].get("version") is None and j_list[i].get("author") is None and EXPERIMENTAL == False:
            logo_txt = ""
        elif j_list[i].get("version") is None and EXPERIMENTAL == True:
            logo_txt = f" | This version is Experimental, there might be bugs! | {author}!"
        elif j_list[i].get("author") is None and EXPERIMENTAL == True:
            logo_txt = f"{version} | This version is Experimental, there might be bugs!"
        elif j_list[i].get("version") is None and EXPERIMENTAL == False:
            logo_txt = f"{author}"
        elif j_list[i].get("author") is None and EXPERIMENTAL == False:
            logo_txt = f"{version}"
        elif EXPERIMENTAL == True:
            logo_txt = "This version is Experimental, there might be bugs!"
        else:
            logo_txt = f"{version} | This version is Experimental, there might be bugs! | {author}"

        def hash_password(password):
            return hashlib.sha256(password.encode('utf-8')).hexdigest()
        subprocess.run(CLEAR_COMMAND, shell=True)
        
        for user in j_list[i].get("users", []):
            users_list.append(user["username"])

        error_msg = ""

        def log_in(username: str = "", logged_in: bool = False):
            if logged_in == True and username != "":
                terminal()
            elif username == "":
                if no_user_interface:
                    print("Unable to log in: Username is blank!")
                    logged_in = False
                    log_in(username="", logged_in=logged_in)
            global attempts, max_attempts
            users = j_list[i].get("users", [])
            if users:
                if username == "":
                    user_found = False
                    print(logo)
                    if no_user_interface == True:
                        print(f"Available Users: {users_list}".replace("[", "").replace("]", "").replace("'", ""))
                    if users:
                        if no_user_interface == True:
                            sign_in_user = input("Please enter your username\n>>> ")
                        else:
                            sign_in_user = simpledialog.askstring("Admin Terminal", f"Available Users: {users_list}".replace("[", "").replace("]", "").replace("'", "") + "\nPlease enter your username")
                        for user in users:
                            if user["username"] == sign_in_user and sign_in_user != None:
                                if user["disabled"]:
                                    subprocess.run(CLEAR_COMMAND, shell=True)
                                    print(f"{sign_in_user} is disabled!\nIf this was a mistake, please contact your administrator.")
                                    log_in()
                                subprocess.run(CLEAR_COMMAND, shell=True)
                                print(logo)
                                if no_user_interface == True:
                                    sign_in_pass = input(f"Please enter your password\nType 'forgot-password' to recover account\nIf Master Password was set then you will be prompted to enter such password when recovering an account\n\nUsername Used: {sign_in_user}\n>>> ")
                                else:
                                    sign_in_pass = simpledialog.askstring("Admin Terminal", f"Please enter your password\nType 'forgot-password' to recover account\nIf Master Password was set then you will be prompted to enter such password when recovering an account\n\nUsername Used: {sign_in_user}")
                                if sign_in_pass != "forgot-password":
                                    hashed_sign_in_pass = hash_password(sign_in_pass)
                                    if hashed_sign_in_pass == user["password"]:
                                        user_found = True
                                        subprocess.run(CLEAR_COMMAND, shell=True)
                                        if user["admin"] == True:
                                            if j_list[i].get("master_password") == getpass("Enter the Master Password\n>>> "):
                                                terminal(user=sign_in_user)
                                            else:
                                                subprocess.run(CLEAR_COMMAND, shell=True)
                                                attempts += 1
                                                if max_attempts != 0:
                                                    print(f"{text_decor.color.FAIL}Master Password was Incorrect! Please Try Again.\n{attempts}/{max_attempts} Attempts Used.\nUsername Used: {text_decor.RESET}{sign_in_user}")
                                                else:
                                                    print(f"{text_decor.color.FAIL}Master Password was Incorrect! Please Try Again.\nMaximum Attempts have been disabled for this instance\nUsername Used: {text_decor.RESET}{sign_in_user}")
                                                if attempts == max_attempts:
                                                    subprocess.run(CLEAR_COMMAND, shell=True)
                                                    print(f"{text_decor.color.FAIL}Max Attempts Reached\nPlease contract the admin and restart the terminal and try again.")
                                                    print(text_decor.RESET)
                                                    subprocess.run(PAUSE_COMMAND, shell=True)
                                                    subprocess.run(CLEAR_COMMAND, shell=True)
                                                    sys.exit()
                                                log_in()
                                        else:
                                            terminal(user=sign_in_user)
                                            break
                                    else:
                                        subprocess.run(CLEAR_COMMAND, shell=True)
                                        attempts += 1
                                        if max_attempts != 0:
                                            print(f"{text_decor.color.FAIL}Password was Incorrect! Please Try Again.\n{attempts}/{max_attempts} Attempts Used.\nUsername Used: {text_decor.RESET}{sign_in_user}")
                                        else:
                                            print(f"{text_decor.color.FAIL}Password was Incorrect! Please Try Again.\nMaximum Attempts have been disabled for this instance\nUsername Used: {text_decor.RESET}{sign_in_user}")
                                        if attempts == max_attempts:
                                            subprocess.run(CLEAR_COMMAND, shell=True)
                                            print(f"{text_decor.color.FAIL}Max Attempts Reached\nPlease restart the terminal and try again.")
                                            print(text_decor.RESET)
                                            subprocess.run(PAUSE_COMMAND, shell=True)
                                            subprocess.run(CLEAR_COMMAND, shell=True)
                                            sys.exit()
                                        log_in()
                                else:
                                    subprocess.run(CLEAR_COMMAND, shell=True)
                                if no_user_interface == True:
                                    sign_in_pass = input(f"Please enter your password\nType 'forgot-password' to recover account\nIf Master Password was set then you will be prompted to enter such password when recovering an account\n\nUsername Used: {sign_in_user}\n>>> ")
                                else:
                                    sign_in_pass = simpledialog.askstring("Admin Terminal", f"Please enter your password\nType 'forgot-password' to recover account\nIf Master Password was set then you will be prompted to enter such password when recovering an account\n\nUsername Used: {sign_in_user}")
                elif username != "":
                    sign_in_pass = input("Please enter your password\nType 'forgot-password' to recover account\nIf Master Password was set then you will be prompted to enter such password when recovering an account\n>>> ")
                    if sign_in_pass != "forgot-password":
                        hashed_sign_in_pass = hash_password(sign_in_pass)
                        if hashed_sign_in_pass == user["password"]:
                            user_found = True
                            subprocess.run(CLEAR_COMMAND, shell=True)
                            if user["admin"] == True:
                                if j_list[i].get("master_password") == getpass("Enter the Master Password\n>>> "):
                                    terminal(user=sign_in_user)
                                else:
                                    subprocess.run(CLEAR_COMMAND, shell=True)
                                    attempts += 1
                                    if max_attempts != 0:
                                        print(f"{text_decor.color.FAIL}Master Password was Incorrect! Please Try Again.\n{attempts}/{max_attempts} Attempts Used.\nUsername Used: {text_decor.RESET}{sign_in_user}")
                                    else:
                                        print(f"{text_decor.color.FAIL}Master Password was Incorrect! Please Try Again.\nMaximum Attempts have been disabled for this instance\nUsername Used: {text_decor.RESET}{sign_in_user}")
                                    if attempts == max_attempts:
                                        subprocess.run(CLEAR_COMMAND, shell=True)
                                        print(f"{text_decor.color.FAIL}Max Attempts Reached\nPlease contract the admin and restart the terminal and try again.")
                                        print(text_decor.RESET)
                                        subprocess.run(PAUSE_COMMAND, shell=True)
                                        subprocess.run(CLEAR_COMMAND, shell=True)
                                        sys.exit()
                                    log_in()
                            else:
                                terminal(user=sign_in_user)
                        else:
                            subprocess.run(CLEAR_COMMAND, shell=True)
                            attempts += 1
                            if max_attempts != 0:
                                print(f"{text_decor.color.FAIL}Password was Incorrect! Please Try Again.\n{attempts}/{max_attempts} Attempts Used.\nUsername Used: {text_decor.RESET}{sign_in_user}")
                            else:
                                print(f"{text_decor.color.FAIL}Password was Incorrect! Please Try Again.\nMaximum Attempts have been disabled for this instance\nUsername Used: {text_decor.RESET}{sign_in_user}")
                            if attempts == max_attempts:
                                subprocess.run(CLEAR_COMMAND, shell=True)
                                print(f"{text_decor.color.FAIL}Max Attempts Reached\nPlease restart the terminal and try again.")
                                print(text_decor.RESET)
                                subprocess.run(PAUSE_COMMAND, shell=True)
                                subprocess.run(CLEAR_COMMAND, shell=True)
                                sys.exit()
                            log_in(username=sign_in_user)
                    else:
                        subprocess.run(CLEAR_COMMAND, shell=True)
                        change_password(username=sign_in_user, new_password=input("Enter your new password\n>>> "))
            else:
                if no_user_interface:
                    username = input("There are currently no users, please enter a new username: ")
                    password = input("Please enter a new password: ")
                else:
                    username = simpledialog.askstring("Admin Terminal", "There are currently no users, please enter a new username")
                    if username == None:
                        sys.exit()
                    password = simpledialog.askstring("Admin Terminal", "Please enter a new password")
                create_user(username=username, password=password)

        def create_user(username, password):
            if username == None:
                if no_user_interface:
                    print(f"Unable to create user: username cannot be empty")
                else:
                    messagebox.showerror("Admin Terminal - Error", f"Unable to create user: username cannot be empty")
                if logged_in == False:
                    log_in(username=username)
                else:
                    setting()
            elif username == "":
                if no_user_interface:
                    print(f"Unable to create user: username cannot be empty")
                else:
                    messagebox.showerror("Admin Terminal - Error", f"Unable to create user: username cannot be empty")
                if logged_in == False:
                    log_in(username=username)
                else:
                    setting()
            elif username != None:
                users = j_list[i].get("users", [])
                hashed_password = hash_password(password)  # Hash the password
                user_id = secrets.token_hex(32)
                userDisabled = False
                userAdmin = False
                new_user = {"username": username, "password": hashed_password, "id": user_id, "admin": userAdmin, "disabled": userDisabled}
                users.append(new_user)
                j_list[i]["users"] = users
                with open(SETTINGS_FILE, 'w') as file:
                    # Scary!
                    json.dump(j_obj, file, indent=4)
                print("User added successfully.\nPlease restart the terminal to continue.")
                subprocess.run(PAUSE_COMMAND, shell=True)
                subprocess.run(CLEAR_COMMAND, shell=True)
                sys.exit()
            elif username != "":
                users = j_list[i].get("users", [])
                hashed_password = hash_password(password)  # Hash the password
                user_id = secrets.token_hex(32)
                user_uuid = secrets.token_urlsafe(32)
                userDisabled = False
                userAdmin = False
                new_user = {"username": username, "password": hashed_password, "id": user_id, "uuid": user_uuid, "admin": userAdmin, "disabled": userDisabled}
                users.append(new_user)
                j_list[i]["users"] = users
                with open(SETTINGS_FILE, 'w') as file:
                    # Scary!
                    json.dump(j_obj, file, indent=4)
                print("User added successfully.\nPlease restart the terminal to continue.")
                subprocess.run(PAUSE_COMMAND, shell=True)
                subprocess.run(CLEAR_COMMAND, shell=True)
                sys.exit()
            else:
                if no_user_interface:
                    print(f"Unable to create user: username cannot be empty")
                else:
                    messagebox.showerror("Admin Terminal - Error", f"Unable to create user: username cannot be empty")
                if logged_in == False:
                    log_in(username=username)
                else:
                    setting()

        def ask_master_password(function: str = "terminal()", openAnotherFile: bool = False):
            if openAnotherFile == True:
                subprocess(f"{PY_COMMAND} {WINPATH}")
            function()

        def change_password(username: str, new_password: str, master_password_required: bool):
            print(logo)

            if master_password_required == False:
                users = j_list[i].get("users", [])
                user_found = False

                for user in users:
                    if user["username"] == username:
                        user["password"] = hash_password(new_password)  # Hash the password
                        user_found = True
                        break

                if user_found:
                    j_list[i]["users"] = users
                    with open(SETTINGS_FILE, 'w') as file:
                        # Scary!
                        json.dump(j_obj, file, indent=4)  # Safely write the updated SETTINGS to the file
                    print(f"{username}'s Password has been changed successfully.")
                    subprocess.run(PAUSE_COMMAND, shell=True)
                    if logged_in == True:
                        terminal()
                    else:
                        log_in(username=username)
                else:
                    print("User not found.")
                    if logged_in == True:
                        terminal()
                    else:
                        log_in()
            else:
                if j_list.get["master_password"] != "":
                    print(logo)
                    master_password_prompt = input("You are about to view sensitive information, Please enter the Master Password")
                    if master_password_prompt != j_list["master_password"]:
                        print("Incorrect Master Password. Please Try Again or type \"cancel\" to go back")
                        change_master_password(username=username, new_password=new_password, master_password_required=True)
                    elif master_password_prompt == "cancel":
                        if logged_in == True:
                            terminal()
                        else:
                            log_in()
                    else:
                        print(logo)

                        if master_password_required == False:
                            users = j_list[i].get("users", [])
                            user_found = False

                            for user in users:
                                if user["username"] == username:
                                    user["password"] = hash_password(new_password)  # Hash the password
                                    user_found = True
                                    break

                            if user_found:
                                j_list[i]["users"] = users
                                with open(SETTINGS_FILE, 'w') as file:
                                    # Scary!
                                    json.dump(j_obj, file, indent=4)  # Safely write the updated SETTINGS to the file
                                print(f"{username}'s Password has been changed successfully.")
                                subprocess.run(PAUSE_COMMAND, shell=True)
                                if logged_in == True:
                                    terminal()
                                else:
                                    log_in(username=username)
                            else:
                                print("User not found.")
                                if logged_in == True:
                                    terminal()
                                else:
                                    log_in()

        def error(mode: int = 0):
            "Makes the terminal crash with a specified mode"
            if mode == 0:
                err = "A manual error was called"
                print(f"{text_decor.RESET}")
                subprocess.run(CLEAR_COMMAND, shell=True)
                try:
                    messagebox.showerror("Admin Terminal has Crashed!", f"Admin Terminal has crashed due to a manual exception\nError: {err}")
                except:
                    print(f"Admin Terminal has crashed due to a manual exception\nError: {err}")
                    subprocess.run(PAUSE_COMMAND, shell=True)
                sys.exit()
            elif mode == 1:
                err = "A permission error was called"
                print(f"{text_decor.RESET}")
                subprocess.run(CLEAR_COMMAND, shell=True)
                try:
                    messagebox.showerror("Admin Terminal has Crashed!", f"Admin Terminal has crashed due to a permission denied exception\nError: {err}")
                except:
                    print(f"Admin Terminal has crashed due to a permission denied exception\nError: {err}")
                    subprocess.run(PAUSE_COMMAND, shell=True)
                sys.exit()

        def change_master_password(user: str = "N/A"):
            # Check if the user is an admin
            users = j_list[i].get("users", [])
            user_found = False
            for u in users:
                if u["username"] == user:
                    user_found = True
                    if not u.get("admin", False):  # Check if the user is not an admin
                        messagebox.showerror("Admin Terminal - Permission Error", "You do not have permission to change the master password.")
                        setting(user_settings=user)  # Redirect to settings

            if not user_found:
                print("User not found.")
                subprocess.run(PAUSE_COMMAND, shell=True)
                subprocess.run(CLEAR_COMMAND, shell=True)
                terminal(user)

            if no_user_interface:
                new_password = getpass("Enter the new Master Password: ")
            else:
                new_password = simpledialog("Admin Terminal", "Enter the new Master Password")

            # Hash the new password
            hashed_password = hash_password(new_password)

            # Update the master_password in the j_list
            j_list[i]["master_password"] = hashed_password

            # Write the updated j_list back to the SETTINGS file
            with open(SETTINGS_FILE, "w") as file:
                # Scary!
                json.dump(j_obj, file, indent=4)

            print("The Master Password has been changed successfully.")
            subprocess.run(PAUSE_COMMAND, shell=True)
            terminal(user)

        def terminal(user: str = "N/A"):
            global attempts
            attempts = 0
            global error_msg
            print(logo)
            print(logo_txt)
            if instructions == True:
                print(f"Type 'help', 'patch' or 'info' for more information\nType 'backup' to backup the settings file\nType 'restore' to restore the settings file\nType 'settings' to access the settings")
            if debug == True:
                print(f"{text_decor.color.WARNING}Debug Functionality is Enabled! Admin Terminal May Not Work Properly!{text_decor.RESET}")
            print(error_msg)
            match input(f">>> {text_decor.color.OKCYAN}"):
                case "info":
                    print(f"{text_decor.RESET}")
                    info(user=user)
                case "file":
                    print(f"{text_decor.RESET}")
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print("Loading File Mode")
                    load_process(5)
                    fileMode(user=user)
                case "patch":
                    print(f"{text_decor.RESET}")
                    patch_notes(user=user)
                case "help":
                    print(f"{text_decor.RESET}")
                    assist(user=user)
                case "?":
                    print(f"{text_decor.RESET}")
                    assist(user=user)
                case "assist":
                    print(f"{text_decor.RESET}")
                    assist(user=user)
                case "settings":
                    print(f"{text_decor.RESET}")
                    setting(user_settings=user)
                case "backup":
                    print(f"{text_decor.RESET}")
                    backup(user=user)
                case "restore":
                    print(f"{text_decor.RESET}")
                    restore(user=user)
                case _:
                    print(f"{text_decor.RESET}")
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    error_msg = f"{text_decor.color.FAIL}Unknown Command\nPlease check if the command exists or you have permission to use it{text_decor.RESET}\n"
                    terminal(user)
            subprocess.run(CLEAR_COMMAND, shell=True)
            print(f"{text_decor.RESET}")

        def backup(user: str = "N/A"):
            subprocess.run(CLEAR_COMMAND, shell=True)
            print(logo)
            if not os.path.exists("backups"):
                os.mkdir("backups")
            fileTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")[:-3]
            backupPath = fr"{WINPATH}\backups\settings_backup_{fileTime}.json"
            SETTINGS_FILEBackup = open(backupPath, "a")
            file = open(SETTINGS_FILE, "r")
            for line in file:
                SETTINGS_FILEBackup.write(line)
            print(f"Waiting for SETTINGS Backup\nPath: {WINPATH}/backups/{backupPath}")
            print(logo)
            load_process(10, "Creating Backup for Settings File...")
            subprocess.run(CLEAR_COMMAND, shell=True)
            print(logo)
            print("SETTINGS have been Backed Up!\nPlease restart the terminal to take effect")
            SETTINGS_FILEBackup.close()
            s_file.close()
            subprocess.run(PAUSE_COMMAND, shell=True)

        def restore(user: str = "N/A"):
            try:
                subprocess.run(CLEAR_COMMAND, shell=True)
                print(logo)
                backupPath = input("Where would you like to restore the SETTINGS file from?\nIt will be from the backups folder\nWill automatically be JSON\n>>> ")
                shutil.copy(f"{WINPATH}\\backups\\{backupPath}.json", SETTINGS_FILE)
                print(f"Preparing for settings file Restore\nPath: {WINPATH}/backups/{backupPath}")
                load_process(10)
                subprocess.run(CLEAR_COMMAND, shell=True)
                print(logo)
                print("SETTINGS have been Restored!\nPlease restart the terminal to take effect")
                subprocess.run(PAUSE_COMMAND, shell=True)
                sys.exit()
            except FileNotFoundError:
                subprocess.run(CLEAR_COMMAND, shell=True)
                print(logo)
                print(f"Unable to restore SETTINGS file!\nFile '{backupPath}' was not found\nPlease try again later.")
                subprocess.run(PAUSE_COMMAND, shell=True)
                terminal(user)

        def setting(user_settings: str = "N/A"):
            subprocess.run(CLEAR_COMMAND, shell=True)
            print(logo)
            print(f"Current User: {user_settings}")
            match input(f"Welcome to the Admin Terminal SETTINGS\nAvailable Options:\n- change-master-password (Will require Master Password if set)\n- set-log-in-attempts\n- change-password\n- reset-settings\n- show-settings\n- add-user\n- switch-logo\n-show_path - Shows the path to the Settings File\n\nLeave blank to go back to main menu\n>>> "):
                case "show_path":
                    if no_user_interface:
                        print(SETTINGS_FILE)
                        setting(user_settings=user_settings)
                    else:
                        messagebox.showinfo("Admin Terminal", f"The Path for the Settings File is: {SETTINGS_FILE}")
                        setting(user_settings=user_settings)

                case "change-password":
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    change_password(username=user_settings, new_password=input("Enter a new password: "))

                case "change-master-password":
                    change_master_password(user=user_settings)

                case "set-log-in-attempts":
                    global max_attempts
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print(logo)
                    if max_attempts != 0:
                        print(f"Current Max Attempts: {max_attempts}")
                    elif max_attempts == 0:
                        print(f"Current Max Attempts: Disabled")
                    editMaxAttempts = int(input("Enter attempts to modify\n>>> "))
                    file = open(SETTINGS_FILE, "w")
                    if editMaxAttempts == 0:
                        j_list[i]["max_attempts"] = editMaxAttempts
                        print("Max Attempts Disabled")
                    elif editMaxAttempts > 0:
                        j_list[i]["max_attempts"] = editMaxAttempts
                        print(f"Max Attempts Set to {editMaxAttempts} attempts")
                    elif editMaxAttempts < 0:
                        print("Max Attempts can not be negative")
                    else:
                        print("Max Attempts was not able to be set")
                    subprocess.run(PAUSE_COMMAND, shell=True)
                    s_file.close()
                    log_in()

                case "add-user":
                    if no_user_interface:
                        create_user(username=input("Enter a new username\n>>>"), password=input("Enter a new password\n>>>"))
                    else:
                        create_user(username=simpledialog.askstring("Admin Terminal", "Enter a new username"), password=simpledialog.askstring("Admin Terminal", "Enter a new password"))

                case "reset-settings":
                    subprocess.run(CLEAR_COMMAND)
                    print(logo)
                    if no_user_interface:
                        user_input = input("Admin Terminal - settings Reset\nAre you sure you want to reset ALL settings?\nThis action can not be undone. (y/n)\n>>> ")
                        if user_input == "y":
                            file = open(SETTINGS_FILE, "w+")
                            s_file.close()
                        else:
                            setting(user_settings=user_settings)
                    else:
                        user_input = messagebox.askyesno("Admin Terminal - settings Reset", "Are you sure you want to reset ALL settings?\nThis action can not be undone.", icon="warning")
                        if user_input == True:
                            file = open(SETTINGS_FILE, "w+")
                            s_file.close()
                        else:
                            setting(user_settings=user_settings)
                    s_file.write("")
                    print("Preparing for settings File reset. . .")
                    load_process(10)
                    s_file.write(SETTINGS)
                    s_file.close()
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print(logo)
                    print("Preparing for settings file reset. . .")
                    load_process(10)
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print(logo)
                    print("settings file has been reset!\n\nReset the terminal for changes to take effect")
                    subprocess.run(PAUSE_COMMAND, shell=True)
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    sys.exit()

                case "show-settings":
                    subprocess.run(CLEAR_COMMAND)
                    subprocess.run(f"{TYPE_COMMAND} settings.json", shell=True)
                    print(j_list[i].get("settings"))
                    subprocess.run(PAUSE_COMMAND, shell=True)
                    setting(user_settings=user_settings)

                case "switch-logo":
                    show_legacy_logo = j_list[i].get("show_legacy_logo")
                    print(logo)

                    if not show_legacy_logo:
                        if no_user_interface:
                            ans = input("Would you like to show the Legacy logo? (Pre 1.4) (y/n): ").strip().lower()
                            if ans == "y":
                                j_list[i]["show_legacy_logo"] = True
                                with open(SETTINGS_FILE, "w") as settings_file:
                                    # Scary!
                                    json.dump(j_obj, settings_file, indent=4)
                                print("The Legacy Logo has been enabled. Please restart the terminal for changes to take effect.")
                                subprocess.run(PAUSE_COMMAND, shell=True)
                                subprocess.run(CLEAR_COMMAND, shell=True)
                                sys.exit()
                            else:
                                setting(user_settings=user_settings)
                        else:
                            ans = messagebox.askyesno("Admin Terminal (Legacy)", "Would you like to show the Legacy logo? (Pre 1.4)")
                            if ans:
                                j_list[i]["show_legacy_logo"] = True
                                with open(SETTINGS_FILE, "w") as settings_file:
                                    # Scary!
                                    json.dump(j_obj, settings_file, indent=4)
                                messagebox.showinfo("Admin Terminal (Legacy)", "The Legacy Logo has been enabled. Please restart the terminal for changes to take effect.")
                                subprocess.run(PAUSE_COMMAND, shell=True)
                                subprocess.run(CLEAR_COMMAND, shell=True)
                                sys.exit()
                            else:
                                setting(user_settings=user_settings)
                    else:
                        if no_user_interface:
                            ans = input("Would you like to show the Modern logo? (Post 1.4) (y/n): ").strip().lower()
                            if ans == "y":
                                j_list[i]["show_legacy_logo"] = False
                                with open(SETTINGS_FILE, "w") as settings_file:
                                    # Scary!
                                    json.dump(j_obj, settings_file, indent=4)
                                print("The Modern Logo has been enabled. Please restart the terminal for changes to take effect.")
                                subprocess.run(PAUSE_COMMAND, shell=True)
                                subprocess.run(CLEAR_COMMAND, shell=True)
                                sys.exit()
                            else:
                                setting(user_settings=user_settings)
                        else:
                            ans = messagebox.askyesno("Admin Terminal", "Would you like to show the Modern logo? (Post 1.4)")
                            if ans:
                                j_list[i]["show_legacy_logo"] = False
                                with open(SETTINGS_FILE, "w") as settings_file:
                                    # Scary!
                                    json.dump(j_obj, settings_file, indent=4)
                                messagebox.showinfo("Admin Terminal", "The Modern Logo has been enabled. Please restart the terminal for changes to take effect.")
                                subprocess.run(PAUSE_COMMAND, shell=True)
                                subprocess.run(CLEAR_COMMAND, shell=True)
                                sys.exit()
                            else:
                                setting(user_settings=user_settings)

                case "":
                    terminal(user_settings)
                case _:
                    setting(user_settings=user_settings)

        def assist(user: str = "N/A"):
            subprocess.run(CLEAR_COMMAND, shell=True)
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
        SETTINGS - Brings up SETTINGS menu
        backup - Backs Up the SETTINGS File
        restore - Restores the SETTINGS File Backup to the SETTINGS File

    File Mode Commands:
        create - Creates files/folders in a specified directory
        exit - Exits File Mode

    SETTINGS Menu:
        set-password - Sets the password
        reset-SETTINGS - Resets the SETTINGS file
        show-SETTINGS - Shows the raw json SETTINGS

    If in File Mode, you can restart or type "exit" the Terminal to exit File Mode''')
            subprocess.run(PAUSE_COMMAND, shell=True)
            subprocess.run(CLEAR_COMMAND, shell=True)
            terminal(user=user)

        def patch_notes(user: str = "N/A"):
            subprocess.run(CLEAR_COMMAND, shell=True)
            print(logo)
            print(f'''{version}
    Patch Notes:
    -   Re-added the legacy logo and can be turned on via the settings
    -   Updated to Python 3.13
    -   Updated the log in system (You can still log in the same way)
    -   Fixed a few bugs''')
            subprocess.run(PAUSE_COMMAND, shell=True)
            subprocess.run(CLEAR_COMMAND, shell=True)
            terminal(user)

        def info(user: str = "N/A"):
            subprocess.run(CLEAR_COMMAND, shell=True)
            print(logo)
            print(f'''{logo_txt}
    Software is open source, you can edit and customize and modify it anyway you want.
    Check out the github at https://github.com/Gh053d413x/Admin_Terminal''')
            subprocess.run(PAUSE_COMMAND, shell=True)
            subprocess.run(CLEAR_COMMAND, shell=True)
            terminal(user)

        def fileMode(user: str = "N/A"):
            subprocess.run(CLEAR_COMMAND, shell=True)
            print(logo)
            try:
                pathInput = input(f"{logo}\nFile Mode\nEnter a file path or type 'exit' to exit\n>>> ")
                if pathInput == "exit":
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print(logo)
                    print("Exiting File Mode")
                    load_process(5)
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    terminal(user)
                elif pathInput != "":
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print(logo)
                    choice0 = input(f"{logo}\nFile Mode\nTo exit type 'exit'\nPath: {pathInput}\nAvailable Choices:\n- create\n- exit\n>>> ")
                    if choice0 == "exit":
                        subprocess.run(CLEAR_COMMAND, shell=True)
                        print(logo)
                        print("Exiting File Mode")
                        load_process(5)
                        subprocess.run(CLEAR_COMMAND, shell=True)
                        terminal(user)
                    elif choice0 == "create":
                        subprocess.run(CLEAR_COMMAND, shell=True)
                        print(logo)
                        choice1 = input(f"{logo}\nFile Mode\nPath: {pathInput}\nWhat do you want to do?\nAvailable Choices:\n- folder\n- file\n>>> ")
                        if choice1 == "file":
                            file = open(pathInput, "w")
                            s_file.close()
                            fileMode()
                        elif choice1 == "folder":
                            os.mkdirs(pathInput)
                            fileMode()
                        elif choice1 == "-file":
                            file = open(pathInput, "w")
                            s_file.close()
                            fileMode()
                        elif choice1 == "-folder":
                            os.mkdirs(pathInput)
                            fileMode()
                        if choice1 == "- file":
                            file = open(pathInput, "w")
                            s_file.close()
                            fileMode()
                        elif choice1 == "- folder":
                            os.mkdirs(pathInput)
                            fileMode()
                        else:
                            subprocess.run(CLEAR_COMMAND, shell=True)
                            print(logo)
                            print(f"{choice1} is not a valid choice")
                            subprocess.run(PAUSE_COMMAND, shell=True)
                            fileMode()
                    else:
                        subprocess.run(CLEAR_COMMAND, shell=True)
                        print(logo)
                        print(f"{choice0} is not a valid choice")
                        subprocess.run(PAUSE_COMMAND, shell=True)
                        fileMode()
                elif pathInput == "":
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print(logo)
                    print("Folder/File path can not be empty")
                    subprocess.run(PAUSE_COMMAND, shell=True)
                    fileMode()
            except Exception as err:
                subprocess.run(CLEAR_COMMAND, shell=True)
                print(logo)
                print(f"An Error Occurred! Error: {err}")
                subprocess.run(PAUSE_COMMAND, shell=True)
                fileMode()
        if __name__ == "__main__":
            if len(sys.argv) > 1:
                match sys.argv[1]:
                    case "--debug":
                        print("Debug Mode Activated!")
                        print("Logging in with DEBUG user.")
                        print("User ID: ", secrets.token_hex(32))
                        logged_in = True
                        log_in(username=None,logged_in=logged_in)
            else:
                log_in(username="",logged_in=False)

    except Exception as err:
        print(f"{text_decor.RESET}")
        subprocess.run(CLEAR_COMMAND, shell=True)
        lineNum = traceback.format_exc()
        try:
            messagebox.showerror("Admin Terminal has Crashed!", f"Admin Terminal has crashed due to an unhandled exception\nError: {err}\n\nFull Error: {lineNum}")
        except:
            print(f"Admin Terminal has crashed due to an unhandled exception\nError: {err}\n\nFull Error: {lineNum}")
            subprocess.run(PAUSE_COMMAND, shell=True)
        sys.exit()
    except KeyboardInterrupt:
        subprocess.run(CLEAR_COMMAND, shell=True)
        print(text_decor.RESET)
        try:
            s_file.close()
            quit()
        except:
            quit()
except Exception as err:
    import traceback
    lineNum = traceback.format_exc()
    try:
        from tkinter import messagebox
        noGUI = False
    except:
        noGUI = True
    
    if noGUI == True:
        print("Admin Terminal was unable to start with the error:")
        print(f"{err}")
        print(f"\"{lineNum}\"")
    else:
        print("Admin Terminal was unable to start with the error:")
        print(f"{err}")
        messagebox.showerror("Python", f"Unable to start Admin Terminal with the error:\n{err}\n\nExact Error:\n{lineNum}")
    
    exit()
    quit()