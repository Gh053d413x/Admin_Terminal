# Admin Terminal Alpha 1.8
# Updated to Python 3.13!
# Made by Ghosted Alex
# Software is free, you can edit and customize and modify it anyway you want.
# Also add Modding Support
# 
# Patch Notes:
# -   Re-added the legacy logo and can be turned on via the settings
# -   Updated to Python 3.13
# -   Updated the log in system (You can still log in the same way)
# -   Fixed a few bugs
# -   Changed the look of constant variables
# -   Fixed the wrong color bug - Some pages had the Blue Hue for input for the main page
# -   Fixed the Settings Wipe bug - Changing a user's password and/or enable/disable-ing the legacy logo would wipe the settings file
# 
# Technical Changes
# -   Added the TYPE_COMMAND variable - Use this to type file contents into the terminal at will
# -   Updated `text_decor.style.END` to `text_decor.RESET`
# -   Renamed `adminPassword` to `master_password`
# -   Added `NoReturn` from the `typing` package
# -   Renamed py_command, clear_command, pause_command and remove_command to PY_COMMAND, CLEAR_COMMAND, PAUSE_COMMAND and REMOVE_COMMAND

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
import traceback
import json
from os.path import exists
from pathlib import Path
import shutil
import datetime
from getpass import getpass
import hashlib

if os.name == "posix":
    PY_COMMAND = "python3"
    CLEAR_COMMAND = "clear"
    PAUSE_COMMAND = "/bin/bash -c 'read -s -n 1 -p \"Press any key to continue...\"'"
    REMOVE_COMMAND = 'rm'
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
            "version": "Alpha 1.8",
            "show_legacy_logo": false,
            "author": "Made by Ghosted Alex",
            "show_instructions": true,
            "max_log_in_attempts":3,
            "users":[
            
            ]
        }
    ]
}"""

inp = ""

winPath = Path.cwd()

# dependenciesExist:
SETTINGS_FILE_EXISTS = exists(fr"{winPath}\settings.json")

# files
SETTINGS_FILE = fr"{winPath}\settings.json"

# functions
def load_process(total):
    subprocess.run(CLEAR_COMMAND, shell=True)
    for i in range(total+1):
        time.sleep(random.uniform(0.1, 0.5))
        percent_complete = (i / total) * 100
        print('\r[' + '#'*i + '='*(total-i) + f'] {percent_complete:.2f}%', end='')

def install_module(package: str = "pip") -> NoReturn:
    global inp
    if inp == "":
        inp = input("WARNING!\nEssential Modules are not installed, limits will be in place for security purposes if essential modules do not get installed, meaning:\n- Updates will not be installed\n- Some functions won't work properly\nWould you like to install them? (y/n)\n>>> ")
    if inp == "n":
        sys.exit()
    elif inp == "y":
        try:
            subprocess.run(CLEAR_COMMAND, shell=True)
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"{package}"])
            try:
                print("Successfully installed Essential Modules!\nPlease restart the terminal to take effect")
                subprocess.run(PAUSE_COMMAND, shell=True)
                subprocess.run(CLEAR_COMMAND, shell=True)
                sys.exit()
            except subprocess.CalledProcessError:
                subprocess.run(CLEAR_COMMAND, shell=True) 
        except:
            subprocess.run(CLEAR_COMMAND, shell=True)
            print("Failed to install Essential Modules!")
            match input("Would you like to try again? (y/n)\n>>> "):
                case "y":
                    install_module()
                case "n":
                    raise ModuleNotFoundError("Essential Modules were not installed!")
                case _:
                    print("Please enter a valid input")
                    install_module()
    else:
        print("Please enter a valid input")
        install_module()

try:
    try:
        import tkinter as tk
        import tkinter.ttk as ttk
        from tkinter import messagebox
        no_user_interface = None
    except ModuleNotFoundError or ImportError as moduleErr:
        subprocess.run(CLEAR_COMMAND, shell=True)
        print(f"ERROR\nThere was a problem loading specific modules: {moduleErr}\nAttempting to install modules...")
        install_module()
        subprocess.run(PAUSE_COMMAND, shell=True)
        no_user_interface = True

    subprocess.run(CLEAR_COMMAND, shell=True)

    if not SETTINGS_FILE_EXISTS:
        if no_user_interface:
            match input("Admin Terminal - NO SETTINGS FILE!\nSettings file is not installed, would you like to install it? (y/n)\n>>> "):
                case "n":
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print("Unable to install settings file due to user cancellation\nPlease try again later")
                    subprocess.run(PAUSE_COMMAND, shell=True)
                    sys.exit()
                case "y":
                    subprocess.run(CLEAR_COMMAND, shell=True)
                case _:
                    sys.exit()
        else:
            match messagebox.askyesno("Admin Terminal - NO SETTINGS FILE!", "SETTINGS file is not installed, would you like to install it?", icon="warning"):
                case False:
                    messagebox.showerror("Admin Terminal - Error", "Unable to install settings file due to user cancellation\nPlease try again later")
                    sys.exit()
                case None:
                    messagebox.showerror("Admin Terminal - Error", "Unable to install settings file due to user cancellation\nPlease try again later")
                    sys.exit()
                case _:
                    with open(SETTINGS_FILE, "w+") as file:
                        file.write(SETTINGS)
                        print("Preparing for settings file download. . .")
                        load_process(10)
                        subprocess.run(CLEAR_COMMAND, shell=True)
    else:
        subprocess.run(CLEAR_COMMAND, shell=True)
    
    # LaunchVars
    show_instructions = False

    file = open(SETTINGS_FILE, "r")

    j_data = file.read()
    j_obj = json.loads(j_data)
    j_list = j_obj["settings"]

    for i in range(len(j_list)):
        if j_list[i]:
            if j_list[i].get("show_instructions") == True:
                show_instructions = True

    if j_list[i]["max_log_in_attempts"] >= 0:
        max_attempts = j_list[i].get("max_log_in_attempts")
    else:
        if no_user_interface == False:
            messagebox.showerror("Admin Terminal Error", "The Maximum Attempts can not be lower than 0. Please set the number equal to or higher than 0\n0 - Disables Max Log In Attempts\n1 and above - Sets Log In Attempts to set number")
            sys.exit()
        else:
            print(f"{text_decor.color.FAIL}The Maximum Attempts can not be lower than 0. Please set the number equal to or higher than 0\n0 - Disables Max Log In Attempts\n1 and above - Sets Log In Attempts to set number{text_decor.RESET}")

    attempts = 0
                    
    version = j_list[i].get("version")
    author = j_list[i].get("author")

    #vars
    match j_list[i]["show_legacy_logo"]:
        case False:
            logo = r"""  ___       _             _          _____                         _                _ 
 / _ \     | |           (_)        |_   _|                       (_)              | |
/ /_\ \  __| | ________   _  ____     | |    ___  ____  ________   _  ____    ____ | |
|  _  | / _  ||  _   _ \ | ||  _ \    | |   / _ \|  __||  _   _ \ | ||  _ \  / _  || |
| | | || (_| || | | | | || || | | |   | |  |  __/| |   | | | | | || || | | || (_| || |
\_| |_/ \__,_||_| |_| |_||_||_| |_|   \_/   \___||_|   |_| |_| |_||_||_| |_| \__,_||_|"""
        case True:
            logo = r"""             _           _         _______                  _             _ 
    /\      | |         (_)       |__   __|                (_)           | |
   /  \   __| |________  _ ____      | | ___ ____ ________  _ ____   ____| |
  / /\ \ / _  |  _   _ \| |  _ \     | |/ _ \  __|  _   _ \| |  _ \ / _  | |
 / ____ \ (_| | | | | | | | | | |    | |  __/ |  | | | | | | | | | | (_| | |
/_/    \_\____|_| |_| |_|_|_| |_|    |_|\___|_|  |_| |_| |_|_|_| |_|\____|_|"""
        case _:
            logo = "<No settings support a logo>"

    print("\n")

    if j_list[i].get("version") is None and j_list[i].get("author") is None:
        logo_txt = ""
    elif j_list[i].get("version") is None:
        logo_txt = f"{author}"
    elif j_list[i].get("author") is None:
        logo_txt = f"{version}"
    else:
        logo_txt = f"{version} | {author}"

    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    subprocess.run(CLEAR_COMMAND, shell=True)

    def update_settings_file():
        ...

    error_msg = ""
    def log_in():
        global attempts, max_attempts
        users = j_list[i].get("users", [])
        user_found = False
        print(logo)
        print("Type in your username and password")
        if users:
            sign_in_user = input("Please enter your username\n>>> ")
            for user in users:
                if user["username"] == sign_in_user:
                    if user["disabled"]:
                        subprocess.run(CLEAR_COMMAND, shell=True)
                        print(f"{sign_in_user} is disabled!\nIf this was a mistake, please contact your administrator.")
                        log_in()
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print(logo)
                    print("Type in your username and password")
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
                        change_password(username=sign_in_user, new_password=input("Enter your new password\n>>> "))
            if not user_found:
                subprocess.run(CLEAR_COMMAND, shell=True)
                print(f"Username '{sign_in_user}' was Not Found!\nPlease try again.")
                log_in()
        else:
            username = input("There are currently no users, please enter a new username: ")
            password = input("Please enter a new password: ")
            create_user(username=username, password=password)

    def create_user(username, password):
        users = j_list[i].get("users", [])
        hashed_password = hash_password(password)  # Hash the password
        userDisabled = False
        userAdmin = False
        new_user = {"username": username, "password": hashed_password, "admin": userAdmin, "disabled": userDisabled}
        users.append(new_user)
        j_list[i]["users"] = users
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(j_obj, file, indent=4)
        print("User added successfully.")
        subprocess.run(PAUSE_COMMAND, shell=True)
        subprocess.run(CLEAR_COMMAND, shell=True)
        log_in()

    def change_password(username: str, new_password: str, master_password_required: bool):
        print(logo)
        if j_list[i].get("master_password") != "":
            passw = getpass("You are about to access sensitive information, please enter the master password\n>>> ")
            hashed_passw = hash_password(passw)
            if hashed_passw != j_list[i].get("master_password"):
                error(1)

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
                json.dump(j_obj, file, indent=4)  # Safely write the updated SETTINGS to the file
            print(f"{username}'s Password has been changed successfully.")
            subprocess.run(PAUSE_COMMAND, shell=True)
            log_in()
        else:
            print("User not found.")
            terminal(user)

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
                
        new_password = getpass("Enter a new Master Password: ")

        # Hash the new password
        hashed_password = hash_password(new_password)

        # Update the master_password in the j_list
        j_list[i]["master_password"] = hashed_password

        # Write the updated j_list back to the SETTINGS file
        with open(SETTINGS_FILE, "w") as file:
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
        if show_instructions == True:
            print(f"Type 'help', 'patch' or 'info' for more information\nType 'backup' to backup the settings file\nType 'restore' to restore the settings file\nType 'settings' to access the settings")
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
        if not os.path.exists("backups"):
            os.mkdir("backups")
        fileTime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")[:-3]
        backupPath = fr"{winPath}\backups\settings_backup_{fileTime}.json"
        SETTINGS_FILEBackup = open(backupPath, "a")
        file = open(SETTINGS_FILE, "r")
        for line in file:
            SETTINGS_FILEBackup.write(line)
        print(f"Waiting for SETTINGS Backup\nPath: {winPath}/backups/{backupPath}")
        load_process(10)
        subprocess.run(CLEAR_COMMAND, shell=True)
        print("SETTINGS have been Backed Up!\nPlease restart the terminal to take effect")
        SETTINGS_FILEBackup.close()
        file.close()
        subprocess.run(PAUSE_COMMAND, shell=True)

    def restore(user: str = "N/A"):
        try:
            subprocess.run(CLEAR_COMMAND, shell=True)
            backupPath = input("Where would you like to restore the SETTINGS file from?\nIt will be from the backups folder\nWill automatically be JSON\n>>> ")
            shutil.copy(f"{winPath}\\backups\\{backupPath}.json", SETTINGS_FILE)
            print(f"Preparing for settings file Restore\nPath: {winPath}/backups/{backupPath}")
            load_process(10)
            subprocess.run(CLEAR_COMMAND, shell=True)
            print("SETTINGS have been Restored!\nPlease restart the terminal to take effect")
            subprocess.run(PAUSE_COMMAND, shell=True)
            sys.exit()
        except FileNotFoundError:
            subprocess.run(CLEAR_COMMAND, shell=True)
            print(f"Unable to restore SETTINGS file!\nFile '{backupPath}' was not found\nPlease try again later.")
            subprocess.run(PAUSE_COMMAND, shell=True)
            terminal(user)

    def setting(user_settings: str = "N/A"):
        subprocess.run(CLEAR_COMMAND, shell=True)
        print(logo)
        print(f"Current User: {user_settings}")
        match input(f"Welcome to the Admin Terminal SETTINGS\nAvailable Options:\n- change-master-password (Will require Master Password if set)\n- set-log-in-attempts\n- change-password (Will require Master Password if set)\n- reset-settings\n- show-settings\n- add-user\n- switch-logo\n\nLeave blank to go back to main menu\n>>> "):
            case "change-password":
                subprocess.run(CLEAR_COMMAND, shell=True)
                change_password(username=user_settings, new_password=input("Enter a new password: "))

            case "change-master-password":
                change_master_password(user=user_settings)

            case "set-log-in-attempts":
                global max_attempts
                subprocess.run(CLEAR_COMMAND, shell=True)
                if max_attempts != 0:
                    print(f"Current Max Attempts: {max_attempts}")
                elif max_attempts == 0:
                    print(f"Current Max Attempts: Disabled")
                editMaxAttempts = int(input("Enter attempts to modify\n>>> "))
                file = open(SETTINGS_FILE, "w")
                if editMaxAttempts == 0:
                    j_list[i]["max_log_in_attempts"] = editMaxAttempts
                    print("Max Attempts Disabled")
                elif editMaxAttempts > 0:
                    j_list[i]["max_log_in_attempts"] = editMaxAttempts
                    print(f"Max Attempts Set to {editMaxAttempts} attempts")
                elif editMaxAttempts < 0:
                    print("Max Attempts can not be negative")
                else:
                    print("Max Attempts was not able to be set")
                subprocess.run(PAUSE_COMMAND, shell=True)
                file.close()
                log_in()

            case "add-user":
                create_user(username=input("Enter a new username\n>>>"), password=input("Enter a new password\n>>>"))

            case "reset-settings":
                if no_user_interface:
                    user_input = input("Admin Terminal - settings Reset\nAre you sure you want to reset ALL settings?\nThis action can not be undone. (y/n)\n>>> ")
                    if user_input == "y":
                        file = open(SETTINGS_FILE, "w+")
                        file.close()
                    else:
                        setting(user_settings=user_settings)
                else:
                    user_input = messagebox.askyesno("Admin Terminal - settings Reset", "Are you sure you want to reset ALL settings?\nThis action can not be undone.", icon="warning")
                    if user_input == True:
                        file = open(SETTINGS_FILE, "w+")
                        file.close()
                    else:
                        setting(user_settings=user_settings)
                file.write("")
                print("Preparing for settings File reset. . .")
                load_process(10)
                file.write(SETTINGS)
                file.close()
                subprocess.run(CLEAR_COMMAND, shell=True)
                print("Preparing for settings file reset. . .")
                load_process(10)
                subprocess.run(CLEAR_COMMAND, shell=True)
                print("settings file has been reset!\n\nReset the terminal for changes to take effect")
                subprocess.run(PAUSE_COMMAND, shell=True)
                subprocess.run(CLEAR_COMMAND, shell=True)
                sys.exit()

            case "show-settings":
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
        try:
            pathInput = input(f"{logo}\nFile Mode\nEnter a file path or type 'exit' to exit\n>>> ")
            if pathInput == "exit":
                subprocess.run(CLEAR_COMMAND, shell=True)
                print("Exiting File Mode")
                load_process(5)
                subprocess.run(CLEAR_COMMAND, shell=True)
                terminal(user)
            elif pathInput != "":
                subprocess.run(CLEAR_COMMAND, shell=True)
                choice0 = input(f"{logo}\nFile Mode\nTo exit type 'exit'\nPath: {pathInput}\nAvailable Choices:\n- create\n- exit\n>>> ")
                if choice0 == "exit":
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print("Exiting File Mode")
                    load_process(5)
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    terminal(user)
                elif choice0 == "create":
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    choice1 = input(f"{logo}\nFile Mode\nPath: {pathInput}\nWhat do you want to do?\nAvailable Choices:\n- folder\n- file\n>>> ")
                    if choice1 == "file":
                        file = open(pathInput, "w")
                        file.close()
                        fileMode()
                    elif choice1 == "folder":
                        os.mkdirs(pathInput)
                        fileMode()
                    elif choice1 == "-file":
                        file = open(pathInput, "w")
                        file.close()
                        fileMode()
                    elif choice1 == "-folder":
                        os.mkdirs(pathInput)
                        fileMode()
                    if choice1 == "- file":
                        file = open(pathInput, "w")
                        file.close()
                        fileMode()
                    elif choice1 == "- folder":
                        os.mkdirs(pathInput)
                        fileMode()
                    else:
                        subprocess.run(CLEAR_COMMAND, shell=True)
                        print(f"{choice1} is not a valid choice")
                        subprocess.run(PAUSE_COMMAND, shell=True)
                        fileMode()
                else:
                    subprocess.run(CLEAR_COMMAND, shell=True)
                    print(f"{choice0} is not a valid choice")
                    subprocess.run(PAUSE_COMMAND, shell=True)
                    fileMode()
            elif pathInput == "":
                subprocess.run(CLEAR_COMMAND, shell=True)
                print("Folder/File path can not be empty")
                subprocess.run(PAUSE_COMMAND, shell=True)
                fileMode()
        except Exception as err:
            subprocess.run(CLEAR_COMMAND, shell=True)
            print(f"An Error Occurred! Error: {err}")
            subprocess.run(PAUSE_COMMAND, shell=True)
            fileMode()
    if __name__ == "__main__":
        log_in()
    else:
        messagebox.showerror("Admin Terminal - Error", "Unable to load the terminal\nAn external program has tried to open Admin Terminal\nPlease launch the terminal directly")
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
        file.close()
        quit()
    except:
        quit()
