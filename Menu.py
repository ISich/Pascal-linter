# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.filedialog import *
from Linter import *

class Menu():
    def __init__(self):
        self.window = Tk()
        self.file_path = "test.txt"
        self.string_len = int()
        self.empty_lines = int()
        self.tabs_count = int()
        self.block_symbols = list()
        self.menu(self.window)
        self.mainloop(self.window)

    def menu(self, window):
        window.resizable(False, False)
        window.geometry("400x400")
        window.title("Linter")
        window.grab_set()

        label0 = Label(window, text="Linter", font=("Roboto", 20, "bold"))
        label0.pack(side=TOP, pady=10)

        frame1 = Frame(window)
        frame1.pack(fill='x', padx=5, pady=5)
        label1_1 = Label(frame1, text="Max string len: ")
        label1_1.pack(side='left')
        entry1 = Entry(frame1, width=8)
        entry1.insert(END, 30)
        entry1.pack(side='left', fill='x')
        #label1_2 = Label(frame1, text="Текст 1.2")
        #label1_2.pack(side='left')

        frame2 = Frame(window)
        frame2.pack(fill='x', padx=5, pady=5)
        label2_1 = Label(frame2, text="Max empty lines: ")
        label2_1.pack(side='left')
        entry2 = Entry(frame2, width=8)
        entry2.insert(END, 1)
        entry2.pack(side='left', fill='x')
        #label2_2 = Label(frame2, text="Текст 1.2")
        #label2_2.pack(side='left')

        frame3 = Frame(window)
        frame3.pack(fill='x', padx=5, pady=5)
        label3_1 = Label(frame3, text="Tabs count: ")
        label3_1.pack(side='left')
        entry3 = Entry(frame3, width=8)
        entry3.insert(END, 1)
        entry3.pack(side='left', fill='x')
        #label3_2 = Label(frame3, text="Текст 1.2")
        #label3_2.pack(side='left')

        framel1 = Frame(window)
        framel1.pack(fill='x', padx=5, pady=5)
        labell1 = Label(framel1, text="Dont checking lines(write from space):")
        labell1.pack(side='left')

        framel2 = Frame(window)
        framel2.pack(fill='x', padx=5, pady=5)
        entryblock = Entry(framel2, width=50)
        entryblock.pack(side='left', fill='x')

        result_button = Button(window, text="Result", font=("Roboto", 14), width=16,
        command=lambda: self.__do_result(entryblock.get(), entry1.get(), entry2.get(), entry3.get()))
        result_button.pack(side=BOTTOM, pady=10)

        btn_file = Button(window, text="Choose_file", font=("Roboto", 8), width=10,
                               command= self.__choose_file)
        btn_file.pack(side=BOTTOM, pady=10)


    def __choose_file(self):
        filetypes = (("Текстовый файл", "*.txt"),
                     ("Pascal", "*.pas"))
        filename = askopenfilename(title="Открыть файл", initialdir="/",
                                      filetypes=filetypes)
        if filename:
            self.file_path = filename
            return True
        return False

    def __check_entry_len(self, value):
        if value.isdigit():
            value = int(value)
            if value > 0:
                self.string_len = int(value)
                return True
        return False

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

    def __do_result(self, block_lines, string_len, empty_lines, tabs_count):
        if self.__check_entry_len(string_len) and self.__check_entry_lines(empty_lines) \
                and self.__check_entry_tabs(tabs_count) and self.__check_block_symbols(block_lines):
            linter_main(self.block_symbols, self.file_path, self.string_len, self.empty_lines, self.tabs_count)
            self.close_window(self.window)
            self.__show_res()
        else:
            return

    def __show_res(self):
        root = Tk()
        root.title("Errors")
        #root.geometry("400x400")

        text_widget = Text(root, height=10, width=50)
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