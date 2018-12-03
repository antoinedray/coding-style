import os
import re
import sys

argc = len(sys.argv)

# CLASS DEFINITION

class config:
    chk_file = '^.+[.](c|h)$'
    ignore = '^.*((.git/|build/).*|(.git|build))$'

class c:
    HEADER = '\033[95m'
    INFO = '\033[94m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

class data:
    filename = None
    line = None
    nb_line = 0
    len_count = 0
    nb_func = 0
    nb_err = 0
    err = {}

# ! CLASS DEFINITION

def info(msg):
    return c.INFO + c.BOLD + msg + c.ENDC

def warn(msg):
    return c.WARNING + msg + c.ENDC

def fail(msg):
    return c.FAIL + msg + c.ENDC

def match(line, regex):
    reg = re.compile(regex)
    if re.match(reg, line):
        return 1
    return 0

def set_err(data, msg):
    data.nb_err += 1
    if str(data.filename) in data.err:
        if str(data.nb_line) in data.err[data.filename]:
            data.err[str(data.filename)][str(data.nb_line)].append(msg)
        else:
            data.err[str(data.filename)][str(data.nb_line)] = [ msg ]
    else:
        data.err[str(data.filename)] = { str(data.nb_line) : [ msg ] }
    return data

def print_moulinette(data):
    for file in data.err:
        print('\n' + info(('{ ' + file + ' }').center(80, '-')) + '\n')
        for line in data.err[file]:
            print(warn("Line: " + line))
            for msg in data.err[file][line]:
                print('  ' + msg)
    print('\n' + fail(('{ STATS }').center(80, '=')) + '\n')
    print('Total: ' + fail(str(data.nb_err)) + ' error found\n')

def rule_braces(data):
    if match(data.line, "^([ ]*({|})(,|;)?)$"):
        # Bracket is correct
        return 1
    elif match(data.line, "^.*([\"]|[']){1}.*({|}).*([\"]|[']){1}.*$"):
        # Bracket is in string, thus ignored
        return 1
    elif match(data.line, "^[ ]*({|})(,|;)?[ ]*[\\\]"):
        # Bracket is in MACRO function
        return 1
    elif match(data.line, '^.*({|}).*$'):
        return 0
    else:
        return 1

def rule_multi_comments(data):
    if match(data.line, "^(([ ]?\*[ ])|([ ]?\*$))"):
        return 0
    return 1

def rule_no_space_before_comment(data):
    if match(data.line, '^([ ]+[\*]+.*)'):
        return 0
    return 1

def rule_cast(data):
    if match(data.line, "^.*=[ ]*[(].+([ ][*])?[)].+$"):
        return 0
    return 1

def rule_func_num(data):
    rt = 1
    if match(data.line, '^(void|static|int|short|char|struct|long|inline)([^=]+[(][^=]*)$'):
        data.nb_func += 1
        if data.nb_func == 11:
            rt = 0
    return data, rt

def rule_func_len(data):
    rt = 1
    if match(data.line, '^(void|static|int|short|char|struct|long|inline)([^=]+[(][^=]*)$'):
        data.len_count = 1
    elif match(data.line, '^}$'):
        data.len_count = 0
    elif match(data.line, '^([ ]*({|})|[ ]*|[ ]*//.*)$'):
        pass
    elif data.len_count > 0:
        data.len_count += 1
    if data.len_count > 25:
        rt = 0
        data.len_count = 0
    return data, rt

def rules(data):
    data, nb_func_rt = rule_func_num(data)
    data, len_func_rt = rule_func_len(data)
    if not rule_multi_comments(data):
        data = set_err(data, 'Intermediary lines start with ** (5.9)')
    if not rule_no_space_before_comment(data):
        data = set_err(data, 'Comments must not be indented (5.9 bis)')
    if not rule_braces(data):
        data = set_err(data, 'All braces MUST be on their own line. (6.1)')
    if not rule_cast(data):
        data = set_err(data, 'No casts allowed. (8.1)')
    if not nb_func_rt:
        data = set_err(data, 'More than 10 functions in file. (8.9)')
    if not len_func_rt:
        data = set_err(data, 'More than 25 lines in function. (8.10)')
    return data

def readlines(data):
    data.len_count = 0
    data.nb_func = 0
    data.nb_line = 1
    with open(data.filename, "r", encoding="ISO-8859-1") as ins:
        for line in ins:
            data.line = line
            data = rules(data)
            data.nb_line += 1
    return data

def main(data):
    for i in range(1, argc):
        if os.path.isdir(sys.argv[i]):
            for root, dirs, files in os.walk(sys.argv[i]):
                if match(root, config.ignore):
                    dirs[:] = []
                    files[:] = []
                else:
                    for file in files:
                        file = str(file)
                        if match(file, config.chk_file):
                            data.filename = os.path.join(root, file)
                            data = readlines(data)
        else:
            if match(str(sys.argv[i]), config.chk_file):
                data = readlines(sys.argv[i])
    print_moulinette(data)

main(data)