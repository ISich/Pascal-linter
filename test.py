from tkinter import *
from tkinter.filedialog import *
import os
import re


def check_unused_ref(lines, block_lines):
    lines = "".join(lines).split("\n")
    in_var_declaration = False
    variables = {}

    for line in lines:
        stripped_line = line.strip().lower()
        if stripped_line.startswith('var'):
            in_var_declaration = True
        elif stripped_line == "begin":
            in_var_declaration = False

        # ������������ ������ ������ ����� ���������� ����������
        if in_var_declaration:
            # ��������� ������ �� ��������� ����������
            var_names = stripped_line.replace(':', ',').split(',')[:-1]
            if stripped_line.startswith('var') and stripped_line != 'var':
                var_names[0] = var_names[0][4:]
            for var in var_names:
                if var.strip():  # ���������� ������ ������
                    variables[var.strip()] = False

        # ��������� ������������� ���������� � ��������� ����� ����
        else:
            for var in variables:
                if var in stripped_line:
                    variables[var] = True

    # ���������� ������ �������������� ����������
    return [f"unused ref: {var}" for var, used in variables.items() if not used]


def get_result(lines, block_lines):
    splitted = immitate_readlines(lines)
    print(check_unused_ref(splitted, block_lines))


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


get_result('''var qwe: array[1..n] of integer;
var asd: array[1..2] of integer;
begin
asd[1] :=3;
qwe[2] = 7;
end. ''', [])


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
