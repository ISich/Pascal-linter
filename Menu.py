# -*- coding: utf-8 -*-
import os
from tkinter import *
from tkinter.filedialog import *
from tkinter.ttk import Combobox
from Linter import *
from tkinter import Tk, messagebox


class Menu():
    def __init__(self):
        self.window = Tk()
        self.file_paths = list()
        self.string_len, self.use_string_len = int(), StringVar(value="True")
        self.empty_lines, self.use_empty_lines = int(), StringVar(value="True")
        self.tabs_count, self.use_tabs_count = int(), StringVar(value="True")
        self.max_space, self.use_max_space = int(), StringVar(value="True")
        self.identic_type = StringVar(value="CamelCase")
        self.unused_ref = StringVar(value="True")
        self.block_symbols = list()
        self.menu(self.window)

    def menu(self, window):
        window.resizable(False, False)
        window.geometry("400x550")
        window.title("Linter")
        window.grab_set()

        label0 = Label(window, text="Linter", font=("Roboto", 20, "bold"))
        label0.pack(side=TOP, pady=10)

        ans = ["True", "False"]
        frame1 = Frame(window)
        frame1.pack(fill='x', padx=5, pady=5)
        label1_1 = Label(frame1, text="Max string len: ")
        label1_1.pack(side='left')
        entry1 = Entry(frame1, width=8)
        entry1.insert(END, "50")
        entry1.pack(side='left', fill='x')
        combobox1 = Combobox(
            frame1, textvariable=self.use_string_len, values=ans, state='readonly')
        combobox1.pack(fill='x', padx=5, pady=5)

        frame2 = Frame(window)
        frame2.pack(fill='x', padx=5, pady=5)
        label2_1 = Label(frame2, text="Max empty lines: ")
        label2_1.pack(side='left')
        entry2 = Entry(frame2, width=8)
        entry2.insert(END, "1")
        entry2.pack(side='left', fill='x')
        combobox2 = Combobox(
            frame2, textvariable=self.use_empty_lines, values=ans, state='readonly')
        combobox2.pack(fill='x', padx=5, pady=5)

        frame3 = Frame(window)
        frame3.pack(fill='x', padx=5, pady=5)
        label3_1 = Label(frame3, text="Tabs count: ")
        label3_1.pack(side='left')
        entry3 = Entry(frame3, width=8)
        entry3.insert(END, "1")
        entry3.pack(side='left', fill='x')
        combobox3 = Combobox(
            frame3, textvariable=self.use_tabs_count, values=ans, state='readonly')
        combobox3.pack(fill='x', padx=5, pady=5)

        frame4 = Frame(window)
        frame4.pack(fill='x', padx=5, pady=5)
        label4_1 = Label(frame4, text="Max space count: ")
        label4_1.pack(side='left')
        entry4 = Entry(frame4, width=8)
        entry4.insert(END, "1")
        entry4.pack(side='left', fill='x')
        combobox4 = Combobox(
            frame4, textvariable=self.use_max_space, values=ans, state='readonly')
        combobox4.pack(fill='x', padx=5, pady=5)

        frame6 = Frame(window)
        frame6.pack(fill='x', padx=5, pady=5)
        label6 = Label(frame6, text="Check unused ref: ")
        label6.pack(side='left')
        combobox = Combobox(
            frame6, textvariable=self.unused_ref, values=ans, state='readonly')
        combobox.pack(fill='x', padx=5, pady=5)

        frame5 = Frame(window)
        frame5.pack(fill='x', padx=5, pady=5)
        label5_1 = Label(frame5, text="Identic type: ")
        label5_1.pack(side='left')
        days = ["CamelCase", "None"]
        self.identic_type = StringVar(value=days[0])
        combobox = Combobox(
            window, textvariable=self.identic_type, values=days, state='readonly')
        combobox.pack(fill='x', padx=5, pady=5)

        framel1 = Frame(window)
        framel1.pack(fill='x', padx=5, pady=5)
        labell1 = Label(framel1, text="Dont checking lines(write from space):")
        labell1.pack(side='left')

        framel2 = Frame(window)
        framel2.pack(fill='x', padx=5, pady=5)
        entryblock = Entry(framel2, width=50)
        entryblock.pack(side='left', fill='x')

        result_button = Button(window, text="Result", font=("Roboto", 14), width=16,
                               command=lambda: self.__do_result(
            entryblock.get(),
            entry1.get(),
            entry2.get(),
            entry3.get(),
            entry4.get()))
        result_button.pack(side=BOTTOM, pady=10)

        frame_btn = Frame(window)
        frame_btn.pack(fill='x', padx=5, pady=5)
        btn_file = Button(frame_btn, text="Choose_files", font=("Roboto", 8), width=14,
                          command=lambda: self.__choose_files())
        btn_file.pack(side=LEFT, pady=10, padx=50)
        btn_folder = Button(frame_btn, text="Choose_folders", font=("Roboto", 8), width=14,
                            command=lambda: self.__choose_folder())
        btn_folder.pack(side=LEFT, pady=10, padx=50)

        self.mainloop(self.window)

    def __choose_files(self):
        filetypes = (("Pascal", "*.pas"),)
        filenames = askopenfilenames(title="Открыть файлы", initialdir="/",
                                     filetypes=filetypes)
        if filenames:
            self.file_paths += list(filenames)
        self.__remove_doubles_filenames()

    def __choose_folder(self):
        directory = askdirectory(title="Открыть папку", initialdir="/")
        all_files = self.__get_all_files_in_folder(directory)
        self.file_paths += list(filter(lambda name: name.endswith(".pas"), all_files))
        self.__remove_doubles_filenames()

    def __get_all_files_in_folder(self, folder: str) -> [str]:
        file_list = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_list.append(f"{root}/{file}")

        return file_list

    def __check_entry_len(self, value):
        if value.isdigit():
            value = int(value)
            if value > 0:
                self.string_len = int(value)
                return True
        return False
    
    def __remove_doubles_filenames(self):
        self.file_paths = list(dict.fromkeys(self.file_paths))

    def __check_entry_lines(self, value):
        if value.isdigit():
            value = int(value)
            if value >= 0:
                self.empty_lines = int(value)
                return True
        return False

    def __check_entry_tabs(self, value):
        if value.isdigit():
            value = int(value)
            if value >= 0:
                self.tabs_count = int(value)
                return True
        return False

    def __check_block_symbols(self, value):
        value = value.split()
        res = True
        for i in range(len(value)):
            if value[i].isdigit():
                value[i] = int(value[i])
                if value[i] >= 0:
                    continue
            res = False
            return res
        self.block_symbols = value.copy()
        return res

    def __check_max_space(self, value):
        if value.isdigit():
            value = int(value)
            if value >= 0:
                self.max_space = int(value)
                return True
        return False

    def to_bool(self, str):
        if str == "True":
            return True
        else:
            return False

    def __do_result(self, block_lines, string_len, empty_lines, tabs_count, space_count):
        if len(self.file_paths) == 0:
            self.__show_message("You haven't chosen files to analyze")
            return

        if self.__check_block_symbols(block_lines)\
                and (self.__check_entry_len(string_len) or not self.to_bool(self.use_string_len.get()))\
                and (self.__check_entry_lines(empty_lines) or not self.to_bool(self.use_empty_lines.get())) \
                and (self.__check_entry_tabs(tabs_count) or not self.to_bool(self.use_tabs_count.get()))\
                and (self.__check_max_space(space_count) or not self.to_bool(self.use_max_space.get())):
            linter(self.block_symbols, self.identic_type.get(), self.file_paths,
                   self.string_len, self.to_bool(self.use_string_len.get()),
                   self.empty_lines, self.to_bool(self.use_empty_lines.get()),
                   self.tabs_count, self.to_bool(self.use_tabs_count.get()),
                   self.max_space, self.to_bool(self.use_max_space.get()),
                   self.unused_ref.get())
            self.close_window(self.window)
            self.__show_res()
        else:
            return

    def __show_message(self, message):
        root = Tk()
        root.withdraw()  # Скрыть основное окно tkinter
        messagebox.showinfo('Уведомление', message)
        root.mainloop()

    def __show_res(self):
        root = Tk()
        root.title("Errors")
        # root.geometry("400x400")

        text_widget = Text(root, height=20, width=80)
        text_widget.pack(side="left", fill="y")

        scrollbar = Scrollbar(root)
        scrollbar.pack(side="right", fill="y")
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)

        # Добавление примера текста
        example_text = "".join(open("errors.txt", "r").readlines())
        text_widget.insert(END, example_text)

        self.mainloop(root)

    def mainloop(self, window):
        window.mainloop()

    def close_window(self, window):
        window.destroy()
