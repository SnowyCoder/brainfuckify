from enum import Enum

REGISTER_COUNT = 256
REGISTER_MAX = 256
MAX_OP_COUNT = 100_000


class Op(Enum):
    ADD_VAL = 0
    ADD_PTR = 1
    PRINT = 2
    LOOP_BEGIN = 3
    LOOP_END = 4


def __sim_compiled(bcode):
    code_index = 0
    register_index = 0
    result = []
    registers = [0] * REGISTER_COUNT
    op_count = 0

    while code_index < len(bcode):
        op, data = bcode[code_index]

        if op == Op.ADD_VAL:
            registers[register_index] = (registers[register_index] + data) % REGISTER_MAX
        elif op == Op.ADD_PTR:
            register_index = (register_index + data) % REGISTER_COUNT
        elif op == Op.PRINT:
            for i in range(data):
                result.append(chr(registers[register_index]))
        elif op == Op.LOOP_BEGIN:
            if registers[register_index] == 0:
                code_index = data - 1
        elif op == Op.LOOP_END:
            code_index = data - 1

        code_index += 1
        op_count += 1
        if op_count > MAX_OP_COUNT:
            return False, "Code out of time", op_count

    return True, ''.join(result), op_count


def __compile(src):
    bcode = []
    loops = []

    has_print = False

    def add_or_inc_last(op, v):
        if bcode and bcode[-1][0] == op:
            bcode[-1] = (bcode[-1][0], bcode[-1][1] + v)
        else:
            bcode.append((op, v))

    for c in src:
        if c == ',':
            return False, "Cannot receive input"
        elif c == '.':
            add_or_inc_last(Op.PRINT, 1)
            has_print = True
        elif c == '+':
            add_or_inc_last(Op.ADD_VAL, 1)
        elif c == '-':
            add_or_inc_last(Op.ADD_VAL, -1)
        elif c == '>':
            add_or_inc_last(Op.ADD_PTR, 1)
        elif c == '<':
            add_or_inc_last(Op.ADD_PTR, -1)
        elif c == '[':
            loops.append(len(bcode))
            bcode.append((Op.LOOP_BEGIN, -1))
        elif c == ']':
            if not loops:
                return False, "Invalid end loop char"
            begin_index = loops.pop()
            bcode.append((Op.LOOP_END, begin_index))
            bcode[begin_index] = (bcode[begin_index][0], len(bcode))

    if loops:
        return False, "Unclosed loops"

    if not has_print:
        # No output (same as not executing anything)
        return True, []

    return True, bcode


def simulate(code):
    compilation_status, bcode = __compile(code)

    if not compilation_status:
        return False, bcode, 0

    return __sim_compiled(bcode)
