from googletrans import Translator, LANGUAGES
from keyboard import read_key
from os import system, listdir
from os.path import isfile, exists
from sys import exit
from time import sleep
from re import fullmatch
from httpcore._exceptions import ConnectError

system("color 0A")

def print_title():
	print("Filenames Translator\n\nVersion: 1.0\n\nMade by Dragon Master\n\n=====================\n\n")

def translate_filenames(source_folder, file_type, dest_folder, srclang=None, destlang=None):
	if destlang is None:
		destlang = "en"
	files = listdir(source_folder)
	logfile = open(f"{dest_folder}/logs.txt","w",buffering=1)
	for filename in files:
		if (filename.find(f".{file_type}") != -1) or (filename.find(f".{file_type}".upper()) != -1):
			try:
				with open(f"{source_folder}/{filename}", "rb") as file:
					data = file.read()
				if srclang is None:
					translated_name = t.translate(filename.split(".")[0], dest=destlang).text
				elif srclang is not None:
					translated_name = t.translate(filename.split(".")[0], src=srclang, dest=destlang).text
				with open(f"{dest_folder}/{translated_name}.{file_type}","wb", buffering=64) as t_file:
					t_file.write(data)
				log = f"Translated \"{filename}\" to \"{translated_name}.{file_type}\""
				logfile.write(f"{log}\n\n")
				print(f"{log}\n")
			except ConnectError:
				error_log = f"Network interrupted for file {filename}"
				logfile.write(f"{error_log}\n\n")
				print(f"{error_log}\n")
	logfile.write("\nWARNING: A few files may have incorrect translations, may not be translated at all, or may not have been copied due to filename issues. Manually check them before using the files.")
	logfile.close()
	system("color 06")
	print(f"\nSuccessfully written the file {dest_folder}/logs.txt")
	system("color 04")
	print("\n\nWARNING: A few files may have incorrect translations, may not be translated at all, or may not have been copied due to filename issues. Manually check them before using the files.")
	system("color 0A")

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
t = Translator()
while True:
	system("cls") 
	print_title()
	system("color 06")
	print('Note: You have to type it in like this C:\\Games\\Game\\FileFolder without quotation marks.\n')
	system("color 0A")
	while True:
		src = input("Enter Source Folder\n>>> ")
		if exists(src) is not True:
			system("color 04")
			print("Invalid Path\n")
			system("color 0A")
		elif exists(src) is True:
			src.replace("\\","/")
			break
	system("cls") 
	print_title()
	system("color 06")
	print('Note: Only characters and numbers are allowed, no need to add the dot to type the format in.\n')
	system("color 0A")
	while True:
		type = input("Enter File Type\n>>> ")
		if fullmatch(r"[A-Za-z0-9]+", type):
			break
		else:
			system("color 04")
			print("Invalid Format Type\n")
			system("color 0A")
	system("cls") 
	print_title()
	system("color 06")
	print('Note: You have to type it in like this C:\\Games\\Game\\FileFolder without quotation marks.\n')
	system("color 0A")
	while True:
		dest = input("Enter Destination Folder\n>>> ")
		if exists(src) is not True:
			system("color 04")
			print("Invalid Path\n")
			system("color 0A")
		elif exists(src) is True:
			src.replace("\\","/")
			break
	system("cls") 
	print_title()
	print("Loading language codes...")
	sleep(2)
	system("cls")
	print_title()
	system("color 06")
	print("Note: Default for source language is auto detection and for destination language it is English.\n")
	system("color 0A")
	print(f"Language Codes:\n\n{string_0}")
	code_list.append("d")
	while True:
		src_lang = input("Enter Source Language\n>>> ")
		dest_lang = input("\nEnter Destination Language\n>>> ")
		if src_lang not in code_list:
			if dest_lang not in code_list:
				print("Invalid Language Code\n")
		else:
			break
	system("cls") 
	print_title()
	print("Starting the operation...\n")
	sleep(1)
	system("cls")
	print_title()
	if src_lang == "d" and dest_lang != "d":
		translate_filenames(src, type, dest, destlang=dest_lang)
	elif dest_lang == "d" and src_lang != "d":
		translate_filenames(src, type, dest, srclang=src_lang)
	elif ((src_lang != "d") and (dest_lang != "d")):
		translate_filenames(src, type, dest, srclang=src_lang, destlang=dest_lang)
	else:
		translate_filenames(src, type, dest)
	print("\n\nRestart the application? y/n")
	while True:
		sleep(0.5)
		key = read_key()
		if key == "y":
			break
		elif key == "n":
			break
			exit()
		else:
			continue