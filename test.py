from tkinter import *
from tkinter.filedialog import *
import os


def check_empty_lines(lines, block_lines, between_func, posible):
    cur_emt = 0
    ind = 0
    empty = True
    errors = []

    for line in lines:
        if line[-1] == "\n":
            line = line[:-1]
        if len(line.strip()) == 0:
            cur_emt += 1
        else:
            if empty and cur_emt != 0:
                for i in range(cur_emt):
                    if i + 1 not in block_lines:
                        errors.append(
                            f"{'file_path'}: Empty string error in {i+1} line\n")
            elif cur_emt > posible:
                for i in range(cur_emt - posible):
                    if ind-cur_emt+i+1 not in block_lines:
                        errors.append(
                            f"{'file_path'}: Empty string error in {ind-cur_emt+i+1} line\n")
            cur_emt = 0
            empty = False

        ind += 1
    if lines[-1][-1] == '\n':
        cur_emt += 1
    for i in range(cur_emt):
        if len(lines)-cur_emt+i+2 not in block_lines:
            errors.append(
                f"{'file_path'}: Empty string error in {len(lines)-cur_emt+i+2} line\n")
    return errors


def get_result(lines, between_func, block_lines):
    splitted = immitate_readlines(lines)
    print(check_empty_lines(splitted, block_lines, "", between_func))


def test_readlines(filename):
    with open(filename, "r") as f:
        print(f.readlines())


def immitate_readlines(st):
    if "\n" not in st:
        return [st + '\n']
    splitted = st.split('\n')
    for i in range(len(splitted) - 1):
        splitted[i] += "\n"
    return splitted


get_result('''var n,p1,p2,p3,p4:integer;

                   
begin
readln;
end.''', 1, [3])


"""var n,p1,p2,p3,p4:integer;          
begin
readln;
    begin
        readln
    end
        n := 3
  begin
    p1 := 4
  end
end."""
