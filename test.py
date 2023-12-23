from tkinter import *
from tkinter.filedialog import *
import os


def check_space_line(line, space_el, l_s=[], r_s=[',']):
    res = []
    for i in range(len(line)):
        if line[i] in space_el:
            if i != 0:
                if line[i - 1] != " ":
                    res.append(i)
            if i != len(line) - 1:
                if line[i + 1] != " ":
                    res.append(i)
        if line[i] in l_s:
            if i != 0:
                if line[i - 1] != " ":
                    res.append(i)
        if line[i] in r_s:
            if i != len(line) - 1:
                if line[i + 1] != " ":
                    res.append(i)
    return res

def check_space(lines, block_lines, max_space, space_elements):
    errors = []
    ind = 0
    for line in lines:
        ind += 1
        line_err = check_space_line(line, space_elements)
        if check_max_spaces(line, max_space):
            errors.append(f"Space in too much in {ind} line\n")
        for error in line_err:
            if ind not in block_lines:
                errors.append(
                    f"Space error in {ind} line {error} pos by element {line[error]}\n")
    return errors

def check_max_spaces(line, max_spaces):
    for i in range(len(line)):
        if line[i] != " ":
            break
    if " " * (max_spaces + 1) in line[i:]:
        return True
    return False

def get_result(lines, between_func, block_lines):
    splitted = immitate_readlines(lines)
    print(check_space(splitted, block_lines, "", between_func))


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
