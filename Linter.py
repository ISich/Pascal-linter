import re


def check_tabs(file_path, err, block_lines, tabs):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    tab_count = 0
    ind = 0
    errors = []

    for line in lines:
        if line[-1] == "\n":
            line = line[:-1]
        if line.strip() == "begin":
            line0 = "    " * tab_count + "begin"
            tab_count += tabs
        elif line.strip() == "end" or line.strip() == "end." or line.strip() == "end;":
            tab_count -= tabs
            line0 = "    " * tab_count + line.strip()
        else:
            st = 0
            for el in line:
                if el != " ":
                    break
                else:
                    st += 1
            line0 = "    " * tab_count + line[st:]
        if line != line0 and len(line.strip()) != 0 and ind + 1 not in block_lines:
            errors.append(f"Tab error in {ind+1} line\n")

        ind += 1
    return errors


def check_empty_lines(file_path, err, block_lines, between_func, posible):
    with open(file_path, 'r') as file:
        lines = file.readlines()
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
                        errors.append(f"Empty string error in {i+1} line\n")
            elif cur_emt > posible:
                for i in range(cur_emt - posible):
                    if ind-cur_emt+i+1 not in block_lines:
                        errors.append(f"Empty string error in {ind-cur_emt+i+1} line\n")
            cur_emt = 0
            empty = False

        ind += 1
    if lines[-1][-1] == '\n':
        cur_emt += 1
    for i in range(cur_emt):
        if len(lines)-cur_emt+i+2 not in block_lines:
            errors.append(f"Empty string error in {len(lines)-cur_emt+i+2} line\n")
    return errors


def check_space_line(line, space_el, l_s = [], r_s = [',']):
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


def check_max_spaces(line, err, max_spaces):
    for i in range(len(line)):
        if line[i] != " ":
            break
    if " " * (max_spaces + 1) in line[i:]:
        return True
    return False


def check_space(file_path, err, block_lines, max_space, space_elements):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    errors = []
    ind = 0
    for line in lines:
        ind += 1
        line_err = check_space_line(line, space_elements)
        if check_max_spaces(line, err, max_space):
            errors.append(f"{file_path}: Space in too much in {ind} line\n")
        for error in line_err:
            if ind not in block_lines:
                errors.append(f"Space error in {ind} line {error} pos by element {line[error]}\n")
    return errors


def check_lines_len(file_path, err, block_lines, max_len):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    errors = []
    ind = 0
    for line in lines:
        ind += 1
        if line.strip() == 0:
            continue
        if check_line_len(line, max_len):
            if ind not in block_lines:
                errors.append(f"{ind} line in too large: {len(line)} > {max_len}\n")
    return errors


def check_line_len(line, max_len):
    if len(line) > max_len:
        return True
    return False


def check_identificators(file_path, err, block_lines):
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
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line_index, line in enumerate(lines):
        identifiers = re.findall(identifiers_pattern, line)
        for ident in identifiers:
            if not re.match(camel_case_pattern, ident) and ident not in keywords:
                error_string += f"incorrect identifier name {ident} (not in CamelCase)\n"
        if line_index not in block_lines:
            errors.append(error_string)
        error_string = ''
    return errors


def check_unused_ref(file_path, err, block_lines):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    lines = "".join(lines).split("\n")
    in_var_declaration = False
    variables = {}

    for line in lines:
        stripped_line = line.strip().lower()
        if stripped_line.startswith('var'):
            in_var_declaration = True
        elif stripped_line == "begin":
            in_var_declaration = False

        # Обрабатываем строки внутри блока объявления переменных
        if in_var_declaration:
            # Разбиваем строку на отдельные переменные
            var_names = stripped_line.replace(':', ',').split(',')[:-1]
            if stripped_line.startswith('var') and stripped_line != 'var':
                var_names[0] = var_names[0][4:]
            for var in var_names:
                if var.strip():  # Игнорируем пустые строки
                    variables[var.strip()] = False

        # Проверяем использование переменных в остальной части кода
        else:
            for var in variables:
                if var in stripped_line:
                    variables[var] = True

    # Возвращаем список неиспользуемых переменных
    return [f"unused ref: {var}" for var, used in variables.items() if not used]


def write_errors(err, errors):
    for error in errors:
        ind = 0
        err.write(error[ind:])


def linter(block_lines, bloc_lines_type, file_names,
                max_len_string, use_max_len,
                empty_lines, use_empty_count,
                tabs_count, use_tabs_count,
                max_space, use_max_space,
                unused_ref):
    err = open("errors.txt", "w")
    err.write(f"Block lines is: {' '.join([str(i) for i in block_lines])}\n\n")
    for file_name in file_names:
        linter_main(err, block_lines, bloc_lines_type, file_name,
                    max_len_string, use_max_len,
                    empty_lines, use_empty_count,
                    tabs_count, use_tabs_count,
                    max_space, use_max_space,
                    unused_ref)


def linter_main(err, block_lines, bloc_lines_type, file_name,
                max_len_string, use_max_len,
                empty_lines, use_empty_count,
                tabs_count, use_tabs_count,
                max_space, use_max_space,
                unused_ref):
    space_elements = ['+', '-', '*', '/']
    err.write(file_name + "\n")
    if use_empty_count:
        write_errors(err, check_empty_lines(file_name, err, block_lines, 2, empty_lines))
    if use_tabs_count:
        write_errors(err, check_tabs(file_name, err, block_lines, tabs_count))
    if use_max_space:
        write_errors(err, check_space(file_name, err, block_lines, max_space, space_elements))
    if use_max_len:
        write_errors(err, check_lines_len(file_name, err, block_lines, max_len_string))
    if bloc_lines_type != "None":
        write_errors(err, check_identificators(file_name, err, block_lines))
    if unused_ref:
        write_errors(err, check_unused_ref(file_name, err, block_lines))
    err.write("\n")