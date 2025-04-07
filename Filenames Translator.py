# Python 3.12.3
from googletrans import Translator, LANGUAGES # pip install googletrans==4.0.0rc1
from keyboard import read_key # pip install keyboard
from colorama import Fore, Style # pip install colorama
from traceback import format_exc
from os import system, listdir, getcwd
from os.path import isfile, exists
from sys import exit
from time import sleep
from re import fullmatch
from ctypes import windll
from httpcore._exceptions import (
    ConnectError, ConnectTimeout, ProxyError, PoolTimeout, ReadTimeout,
    TimeoutException, NetworkError, WriteTimeout, ProtocolError, CloseError
)

system("title Filenames Translator")

hwnd = windll.kernel32.GetConsoleWindow()
GWL_STYLE = -16
WS_MAXIMIZEBOX = 0x00010000
WS_SIZEBOX = 0x00040000

style = windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
style &= ~(WS_MAXIMIZEBOX | WS_SIZEBOX)
windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027)  # SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED

def printc(string, color="LightGreen", end="\n"):
    if color == "LightGreen":
        print(Fore.LIGHTGREEN_EX + string + Style.RESET_ALL, end)
        return None
    if color == "Red":
        print(Fore.RED + string + Style.RESET_ALL, end)
        return None
    if color == "Yellow":
        print(Fore.YELLOW + string + Style.RESET_ALL, end)
        return None
        
def inputc(string, color="LightGreen"):
    if color == "LightGreen":
        input_text = input(Fore.LIGHTGREEN_EX + string)
    if color == "Red":
        input_text = input(Fore.RED + string)
    if color == "Yellow":
        input_text = input(Fore.YELLOW + string)
    return input_text

def centralize(string, char_limit):
    spaces = char_limit - len(string)
    return ((" " * (spaces // 2)) + string)

def print_title():
    appname = centralize("Filenames Translator", 120)
    ver = centralize("Version: 1.0", 120)
    credit = centralize("Made by Dragon Master", 120)
    printc(appname + "\n\n" + ver + "\n\n" + credit + "\n\n" + ("=" * 120) + "\n\n")

def rename_ifexists(name,folder):
    i = 1
    if name.find(".") == -1:
        return None
    split = name.rsplit(".",1)
    while True:
        if name in listdir(folder):
            name = split[0] + f"({i})" + "." + split[1]
        else:
            return name
        if name in listdir(folder):
            i += 1

def translate_filenames(source_folder, file_type, dest_folder, srclang=None, destlang=None):
    t = Translator()
    file_exists = False
    if destlang is None:
        destlang = "en"
    files = listdir(source_folder)
    logfile = open(f"{dest_folder}/logs.txt","w", encoding="utf-8", buffering=1)
    counter = [0,0]
    for filename in files:
        if (filename.find(f".{file_type}") != -1) or (filename.find(f".{file_type}".upper()) != -1):
            file_exists = True
            with open(f"{source_folder}/{filename}", "rb") as file:
                data = file.read()
            filename = filename.replace("「","(").replace("」",")")
            net_error_log = "N/A"
            try:
                sleep(0.2)
                if srclang is None:
                    translated_name = t.translate(filename.rsplit(".",1)[0], dest=destlang).text
                elif srclang is not None:
                    translated_name = t.translate(filename.rsplit(".",1)[0], src=srclang, dest=destlang).text
                translated_name = translated_name.replace('"','')
                translated_name = rename_ifexists(f"{translated_name}.{file_type}",dest_folder).rsplit(".",1)[0]
            except ConnectError:
                net_error_log = f"Failed to establish a network connection for file \"{filename}\""
            except ConnectTimeout:
                net_error_log = f"Connection to server timed out for file \"{filename}\""
            except ProxyError:
                net_error_log = f"Proxy error encountered for file \"{filename}\""
            except PoolTimeout:
                net_error_log = f"Connection pool timed out for file \"{filename}\""
            except ReadTimeout:
                net_error_log = f"Server took too long to respond for file \"{filename}\""
            except TimeoutException:
                net_error_log = f"Request timed out for file \"{filename}\""
            except NetworkError:
                net_error_log = f"Network error occurred for file \"{filename}\""
            except WriteTimeout:
                net_error_log = f"Request could not be sent in time for file \"{filename}\""
            except ProtocolError:
                net_error_log = f"Protocol error encountered for file \"{filename}\""
            except CloseError:
                net_error_log = f"Error closing connection for file \"{filename}\""
            except Exception:
                log = f"Failed to translate \"{filename}\" due to some errors."
                counter[1] += 1
                printc(f"{log}\n", color="Red")
                logfile.write(f"{log}\n\n")
                continue
            if net_error_log != "N/A":
                logfile.write(f"{net_error_log}\n\n")
                printc(f"{net_error_log}\n", color="Red")
                counter[1] += 1
                continue
            try:
                with open(f"{dest_folder}/{translated_name}.{file_type}","wb", buffering=64) as t_file:
                    t_file.write(data)
                filename = filename.replace("(","「").replace(")","」")
                log = f"Translated \"{filename}\" to \"{translated_name}.{file_type}\""
                printc(f"{log}\n")
            except OSError:
                net_error_log = "ErrorCounterOnly"
                log = f"Translated \"{filename}\" to \"{translated_name}.{file_type}\" but failed to create the file because the translated filename is not supported."
                printc(f"{log}\n", color="Red")
            logfile.write(f"{log}\n\n")
            if net_error_log == "ErrorCounterOnly":
                counter[1] += 1
            elif net_error_log == "N/A":
                counter[0] += 1
                pass
    if file_exists == False:
        printc(f"No file found with the extension: {file_type}\nGiven Destination Folder: {dest_folder}", color="Red")
        return None
    logfile.write(f"\nTotal files renamed successfully: {counter[0]}\nTotal fails: {counter[1]}\n")
    logfile.write("\nWARNING: A few files may have incorrect translations, may not be translated at all, or may not have been copied due to filename issues. Manually check them before using the files.")
    logfile.close()
    printc("-" * 120)
    printc(f"\nSuccessfully written the file {dest_folder}/logs.txt", color="Yellow")
    printc(f"\nTotal files renamed successfully: {counter[0]}")
    printc(f"Total fails: {counter[1]}", color="Red")
    printc("\n\nWARNING: A few files may have incorrect translations, may not be translated at all, or may not have been copied due to\nfilename issues. Manually check them before using the files.", color="Red")

code_list = list(LANGUAGES.keys())
lang_list = list(LANGUAGES.values())
string_0 = ""
c = 0
for lang in lang_list:
    lang_list[c] = lang.title()
    c += 1
c = 0
string_0 += "Default = d\n\n"
while c < len(lang_list):
    string_0 += f"{lang_list[c]} = {code_list[c]}\n\n"
    c += 1
while True:
    system("cls") 
    print_title()
    printc('Note: You have to type it in like this C:\\Games\\Game\\FileFolder without quotation marks. (Spaces can be kept)\n', color="Yellow")
    while True:
        src = inputc("Enter Source Folder\n>>> ")
        if exists(src) is not True:
            printc("\nInvalid Path\n", color="Red")
        elif exists(src) is True:
            src = src.replace("\\","/")
            break
    system("cls") 
    print_title()
    printc('Note: Only characters and numbers are allowed, no need to add the dot to type the extension in.\n', color="Yellow")
    while True:
        type = inputc("Enter File Extension\n>>> ").lower()
        if fullmatch(r"[A-Za-z0-9]+", type):
            break
        else:
            printc("\nInvalid Extension\n", color="Red")
    system("cls") 
    print_title()
    printc('Note: You have to type it in like this C:\\Games\\Game\\FileFolder without quotation marks. Also, keep your destination\nfolder empty. (Spaces can be kept)\n', color="Yellow")
    while True:
        dest = inputc("Enter Destination Folder\n>>> ")
        if exists(dest) is not True:
            printc("\nInvalid Path\n", color="Red")
        elif exists(dest) is True:
            dest = dest.replace("\\","/")
            break
    system("cls") 
    print_title()
    printc("Loading language codes...")
    sleep(1.3)
    system("cls")
    print_title()
    printc("Note: Default for source language is auto detection and for destination language it is English.\n", color="Yellow")
    printc(f"Language Codes:\n\n{string_0}")
    code_list.append("d")
    while True:
        src_lang = inputc("Enter Source Language\n>>> ")
        if src_lang not in code_list:
            printc("\nInvalid Language Code\n", color="Red")
            continue
        else:
            break
    print("")
    while True:
        dest_lang = inputc("Enter Destination Language\n>>> ")
        if dest_lang not in code_list:
            printc("\nInvalid Language Code\n", color="Red")
        else:
            break
    system("cls") 
    print_title()
    printc("Starting the operation...\n")
    sleep(1)
    system("cls")
    print_title()
    try:
       if src_lang == "d" and dest_lang != "d":
           translate_filenames(src, type, dest, destlang=dest_lang)
       elif dest_lang == "d" and src_lang != "d":
           translate_filenames(src, type, dest, srclang=src_lang)
       elif ((src_lang != "d") and (dest_lang != "d")):translate_filenames(src, type, dest, srclang=src_lang, destlang=dest_lang)
       else:
           translate_filenames(src, type, dest)
    except Exception:
       with open("error.log","w") as error:
           error.write(format_exc())
       directory = getcwd().replace("/","\\")
       printc(f"Error occured while running the application. Please send the error.log file to developer.\nLocation: {directory}", color="Red")
    printc("\n\nRestart the application? y/n")
    while True:
        sleep(0.5)
        key = read_key(suppress=True)
        if key == "y":
            del key
            break
        elif key == "n":
            exit()
        else:
            continue
