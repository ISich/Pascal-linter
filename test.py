from tkinter import *
from tkinter.filedialog import *
import os
import re


def check_identificators(lines, block_lines):
    camel_case_pattern = r'^[A-Za-z][a-zA-Z0-9]*$'
    identifiers_pattern = r'\b[a-zA-Z]+\w*\b'
    keywords = [
        'and', 'array', 'begin', 'case', 'const', 'div', 'do', 'downto', 'else',
        'end', 'file', 'for', 'function', 'goto', 'if', 'in', 'label', 'mod', 'nil',
        'not', 'of', 'or', 'packed', 'procedure', 'program', 'record', 'repeat',
        'set', 'then', 'to', 'type', 'unit', 'until', 'uses', 'var', 'while', 'with'
    ]
    error_string = ''
    errors = []
    for line_index, line in enumerate(lines):
        identifiers = re.findall(identifiers_pattern, line)
        for ident in identifiers:
            if not re.match(camel_case_pattern, ident) and ident not in keywords:
                error_string += f"incorrect identifier name {ident} (not in CamelCase)\n"
        if line_index not in block_lines:
            if error_string != '':
                errors.append(error_string)
        error_string = ''
    return errors


def get_result(lines, block_lines):
    splitted = immitate_readlines(lines)
    print(check_identificators(splitted, block_lines))


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


get_result('''CamelCased :=not_cCcC''', [])


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
