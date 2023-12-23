from tkinter import *
from tkinter.filedialog import *
import os


def __choose_folder():
    directory = askdirectory(title="Открыть папку", initialdir="/")
    all_files = __get_all_files_in_folder(directory)
    return list(filter(lambda name: name.endswith(".pas"), all_files))


def __get_all_files_in_folder(folder: str) -> [str]:
    file_list = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            file_list.append(f"{root}/{file}")

    return file_list


print(__choose_folder())
