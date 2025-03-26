nr_instructions = -1


def iota():
    global nr_instructions
    nr_instructions += 1
    return nr_instructions


OP_ADD = iota()
OP_SUB = iota()
OP_INC = iota()
OP_DEC = iota()
OP_CALL = iota()
OP_XOR = iota()
OP_PUSH = iota()
OP_POP = iota()
OP_MOV = iota()
OP_MUL = iota()
OP_DIV = iota()
OP_CMP = iota()
OP_SETE = iota()
OP_RET = iota()
OP_JE = iota()
OP_JNE = iota()
OP_LABEL = iota()
OP_JMP = iota()
