def check_tabs(file_path, err, block_lines, tabs):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    tab_count = 0
    ind = 0

    for line in lines:
        if line[-1] == "\n":
            line = line[:-1]
        if line.strip() == "begin":
            line0 = "    " * tab_count + "begin"
            tab_count += tabs
        elif line.strip() == "end" or line.strip() == "end.":
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
            err.write(f"Tab error in {ind+1} line\n")

        ind += 1


def check_empty_lines(file_path, err, block_lines, between_func, posible):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    cur_emt = 0
    ind = 0
    empty = True

    for line in lines:
        if line[-1] == "\n":
            line = line[:-1]
        if len(line.strip()) == 0:
            cur_emt += 1
        else:
            if empty and cur_emt != 0:
                for i in range(cur_emt):
                    if i + 1 not in block_lines:
                        err.write(f"Empty string error in {i+1} line\n")
            elif cur_emt > posible:
                for i in range(cur_emt - posible):
                    if ind-cur_emt+i+1 not in block_lines:
                        err.write(f"Empty string error in {ind-cur_emt+i+1} line\n")
            cur_emt = 0
            empty = False

        ind += 1
    if lines[-1][-1] == '\n':
        cur_emt += 1
    for i in range(cur_emt):
        if len(lines)-cur_emt+i+2 not in block_lines:
            err.write(f"Empty string error in {len(lines)-cur_emt+i+2} line\n")


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
    ind = 0
    for line in lines:
        ind += 1
        line_err = check_space_line(line, space_elements)
        if check_max_spaces(line, err, max_space):
            err.write(f"Space in too much in {ind} line\n")
        for error in line_err:
            if ind not in block_lines:
                err.write(f"Space error in {ind} line {error} pos by element {line[error]}\n")


def check_lines_len(file_path, err, block_lines, max_len):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    ind = 0
    for line in lines:
        ind += 1
        if line.strip() == 0:
            continue
        if check_line_len(line, max_len):
            if ind not in block_lines:
                err.write(f"{ind} line in too large: {len(line)} > {max_len}\n")


def check_line_len(line, max_len):
    if len(line) > max_len:
        return True
    return False


def linter_main(block_lines, file_name, max_len_string, empty_lines, tabs_count, max_space):
    space_elements = ['+', '-', '*', '/', '=']
    err = open("errors.txt", "w")
    err.write(f"Block lines is: {' '.join([str(i) for i in block_lines])}\n")
    check_empty_lines(file_name, err, block_lines, 2, empty_lines)
    check_tabs(file_name, err, block_lines, tabs_count)
    check_space(file_name, err, block_lines, max_space, space_elements)
    check_lines_len(file_name, err, block_lines, max_len_string)