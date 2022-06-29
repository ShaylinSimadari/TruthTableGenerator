class OrderedDict:

    def __init__(self):
        self.keys = []
        self.values = []

    def put(self, key, val):
        if key not in self.keys:
            self.keys.append(key)
            self.values.append(val)
        else:
            self.values[self.keys.index(key)] = val

    def clear(self):
        self.keys.clear()
        self.values.clear()

    def set_val(self, index, val):
        self.values[index] = val

    def value_of(self, key):
        return self.values[self.keys.index(key)]

    def __len__(self):
        return len(self.keys)


def print_head(primitives, steps):
    string = ''
    for k in primitives.keys:
        string += '|' + k + '\t'

    for k in steps.keys:
        string += '|' + k + '\t'

    print(string[1:], '')


def print_head_ans(primitives, steps):
    string = ''
    for k in primitives.keys:
        string += '|' + k + '\t'

    string += '|' + steps.keys[-1] + '\t'

    print(string[1:], '')


def print_row(primitives, steps):
    string = ''

    for k in primitives.keys:
        v = primitives.value_of(k)
        space = int((len(k) - len(v) + 1) / 4) + 1
        string += '|' + v + ('\t' * space)

    for k in steps.keys:
        v = steps.value_of(k)
        space = int((len(k) - len(v) + 1) / 4) + 1
        string += '|' + v + ('\t' * space)

    print(string[1:], '')


def print_ans(primitives, steps):
    string = ''

    for k in primitives.keys:
        v = primitives.value_of(k)
        space = int((len(k) - len(v) + 1) / 4) + 1
        string += '|' + v + ('\t' * space)

    k = steps.keys[-1]
    v = steps.values[-1]
    space = int((len(k) - len(v) + 1) / 4) + 1
    string += '|' + v + ('\t' * space)

    print(string[1:], '')


primitive_table = OrderedDict()
steps_table = OrderedDict()


def main():
    show_working = False
    while True:
        cmd = "".join(input("input a logical argument: ").split())
        if cmd == 'quit':
            break
        if cmd == 'help':
            print('~ ^ v -> <->', 'use any letter except v for terms', "'quit' to quit")
            continue
        if cmd == 'toggleworking':
            show_working = not show_working
            print("show working", "on" if show_working else "off")
            continue

        #preprocess

        init_base_variables(primitive_table, cmd)
        steps_table.clear()

        analyse(cmd)  # this run through is just to generate the step heads
        if show_working:
            print_head(primitive_table, steps_table)
        else:
            print_head_ans(primitive_table, steps_table)

        for i in range(2 ** len(primitive_table)):
            analyse(cmd)
            if show_working:
                print_row(primitive_table, steps_table)
            else:
                print_ans(primitive_table, steps_table)
            update_base_variable_values(primitive_table, i + 1)


def update_base_variable_values(table, row):
    b = "{0:b}".format(row)
    for j in range(-1, -len(table) - 1, -1):
        if -j <= len(b):
            table.values[j] = b[j]
        else:
            table.values[j] = '0'


def init_base_variables(table, cmd):
    table.clear()
    for i in range(len(cmd)):
        char = cmd[i]
        if is_term(char):
            table.put(char, '0')
    return


def analyse(cmd, indent=0):
    i = 0
    i, p, t1 = calculate_next_term(cmd, i, indent)
    while i < len(cmd):
        i, op = find_op(cmd, i)
        i, q, t2 = calculate_next_term(cmd, i, indent)
        p = calculate(p, q, op)
        t1 = t1 + op + t2
        steps_table.put(t1, p)
    return p


def find_op(cmd, i):
    start = i
    while not (is_open_bracket(cmd[i]) or is_term(cmd[i]) or is_negate(cmd[i])):
        i += 1
    op = (cmd[start:i])
    return i, op


def calculate_next_term(cmd, i, indent):
    if is_negate(cmd[i]):
        op = cmd[i]
        i += 1
        i, q, t = calculate_next_term(cmd, i, indent)
        q = calculate(None, q, op)
        term = op + t
        if term not in primitive_table.keys:
            steps_table.put(term, q)
    elif cmd[i] == '(':
        bracks = 0
        i += 1
        start = i
        while cmd[i] != ')' or bracks != 0:
            if cmd[i] == '(':
                bracks += 1
            elif cmd[i] == ')':
                bracks -= 1
            i += 1
        q = analyse(cmd[start:i], indent + 1)
        i += 1
        term = cmd[start-1:i]
    else:
        q = calculate(None, cmd[i], None)
        i += 1
        term = cmd[i-1]
    return i, q, term


def calculate(p, q, op):
    if op is None:
        return intof(boolof(q))
    if is_negate(op):
        return intof(not boolof(q))
    p = boolof(p)
    q = boolof(q)
    out = False
    if is_and(op):
        out = p and q
    elif is_or(op):
        out = p or q
    elif is_implies(op):
        out = (not p) or q
    elif is_biconditional(op):
        out = p == q
    else:
        print('error', op, p, q)
    return intof(out)


def boolof(char):
    if char == '0':
        return False
    elif char == '1':
        return True
    return boolof(primitive_table.value_of(char))


def intof(boo):
    if boo:
        return '1'
    return '0'


def is_term(char):
    return char != 'x' and char != 'v' and ((96 < ord(char) < 123) or char == '0' or char == '1')


def is_open_bracket(char):
    return char in ['(', '[']


def is_closed_bracket(char):
    return char in [')', ']']


def is_operator(char):
    return is_negate(char) or is_and(char) or is_or(char) or is_implies(char) or is_biconditional(char)


def is_negate(char):
    return char in ['~', '¬', '¬', '!']


def is_and(char):
    return char in ['^', '∧', 'x', '.', '*']


def is_or(char):
    return char in ['v', '∨', '+']


def is_implies(char):
    return char in ['->', '=>']


def is_biconditional(char):
    return char in ['<->', '<=>', '⇔']


main()
