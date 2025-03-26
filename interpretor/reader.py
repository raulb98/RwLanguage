from Instructions_asm.instr_generator import *


"This will map the Word to its index. The index has to be that."
SYNTAX_RULES_INDEX = {
    "QWORD": 0,
    "DWORD": 0,
    "WORD": 0,
    "BYTE": 0,
    "CALL": 0,
    "ADD": 0,
    "SUB": 0,
    "MUL": 0,
    "DIV": 0,
    "EQ": 0,
    "IF": 0,
    "ELSE": 0,
    "ENDIF": 0,
}

SYNTAX_RULES_TYPE = {
    "QWORD": "VARIABLE",
    "DWORD": "VARIABLE",
    "WORD": "VARIABLE",
    "BYTE": "VARIABLE",
    "CALL": "CALL",
    "ADD": "ADD",
    "SUB": "SUB",
    "MUL": "MUL",
    "DIV": "DIV",
    "EQ": "EQ",
    "IF": "IF",
    "ELSE": "ELSE",
    "ENDIF": "ENDIF"
}

REGISTER_PREFIX_BY_LEN = {
    "rax": {
        "QWORD": "rax",
        "DWORD": "eax",
        "WORD": "ax",
        "BYTE": "ah"
    },
    "rbx": {
        "QWORD": "rbx",
        "DWORD": "ebx",
        "WORD": "bx",
        "BYTE": "bh"
    },
    "rcx": {
        "QWORD": "rcx",
        "DWORD": "ecx",
        "WORD": "cx",
        "BYTE": "ch"
    },
    "rdx": {
        "QWORD": "rdx",
        "DWORD": "edx",
        "WORD": "dx",
        "BYTE": "dh"
    }
}

DATA_TYPE_SIZES = {
    "QWORD": 8,
    "DWORD": 4,
    "WORD": 2,
    "BYTE": 1
}

class Reader:
    def __init__(self):
        self.line = ""
        self.state = None
        self.var_name = None
        self.var_value = 0
        self.var_size = 0
        self.depth_rsp_func = 0
        self.var_type = None
        self.var_positions = {}
        self.var_types = {}
        self.var_rez = ""
        self.var_op1 = ""
        self.var_op2 = ""
        self.func_name = None
        self.func_with_var = False
        self.if_start = False
        self.else_start = False
        self.endif_found = False
        self.if_count = 0

    def get_variable_instruction_asm(self):
        list_of_instr = []
        self.depth_rsp_func += self.var_size
        list_of_instr.append(instr_generator(OP_SUB, ["rsp", self.var_size]))
        list_of_instr.append(instr_generator(OP_MOV, ["{} [rbp-{}]".format(self.var_type, str(self.depth_rsp_func)),
                                                      str(self.var_value)]))
        return list_of_instr

    def get_call_instruction_asm(self):
        list_of_instr = []
        if not self.func_with_var:
            list_of_instr.append(instr_generator(OP_PUSH, [str(self.var_value)]))
            list_of_instr.append(instr_generator(OP_CALL, [self.func_name]))
            list_of_instr.append(instr_generator(OP_POP, ["rax"]))
        else:
            var_index = self.var_positions[self.var_name]
            var_type = self.var_types[self.var_name]
            registry_size = REGISTER_PREFIX_BY_LEN["rax"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [registry_size, "{} [rbp-{}]".format(var_type, str(var_index))]))
            list_of_instr.append(instr_generator(OP_PUSH, ["rax"]))
            list_of_instr.append(instr_generator(OP_CALL, [self.func_name]))
            list_of_instr.append(instr_generator(OP_POP, ["rax"]))
        return list_of_instr

    def get_add_instruction_asm(self):
        list_of_instr = []
        if self.var_op1.isnumeric() and self.var_op2.isnumeric():
            print("Cannot add 2 numerics. Only Variable and Variable or Variable and Number!")
            exit(1)
        if self.var_op1.isnumeric():
            print("First Operand Has to be a Variable!")
            exit(1)
        if self.var_rez.isnumeric():
            print("Result in ADD can't be a numeric!")
            exit(1)
        rez_type = self.var_types[self.var_rez]
        res_index = self.var_positions[self.var_rez]
        rez_size_rax = REGISTER_PREFIX_BY_LEN["rax"][rez_type]
        rez_size_rbx = REGISTER_PREFIX_BY_LEN["rbx"][rez_type]
        op1_size = ""
        op2_size = ""

        if not self.var_op1.isnumeric():
            op1_index = self.var_positions[self.var_op1]
            var_type = self.var_types[self.var_op1]
            op1_size = REGISTER_PREFIX_BY_LEN["rax"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op1_size, "{} [rbp-{}]".format(var_type, str(op1_index))]))
            "mov eax, dword [rbp-idx]"

        if not self.var_op2.isnumeric():
            op2_index = self.var_positions[self.var_op2]
            var_type = self.var_types[self.var_op2]
            op2_size = REGISTER_PREFIX_BY_LEN["rbx"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op2_size, "{} [rbp-{}]".format(var_type, str(op2_index))]))
            "mov eax, dword [rbp-idx]"
        else:
            op2_size = int(self.var_op2)
            "mov eax, var"
        list_of_instr.append(instr_generator(OP_ADD, [op1_size, op2_size]))
        list_of_instr.append(instr_generator(OP_MOV, ["{} [rbp-{}]".format(rez_type, res_index), op1_size]))

        return list_of_instr

    def get_sub_instruction_asm(self):
        list_of_instr = []
        if self.var_op1.isnumeric() and self.var_op2.isnumeric():
            print("Cannot add 2 numerics. Only Variable and Variable or Variable and Number!")
            exit(1)
        if self.var_op1.isnumeric():
            print("First Operand Has to be a Variable!")
            exit(1)
        if self.var_rez.isnumeric():
            print("Result in ADD can't be a numeric!")
            exit(1)
        rez_type = self.var_types[self.var_rez]
        res_index = self.var_positions[self.var_rez]
        rez_size_rax = REGISTER_PREFIX_BY_LEN["rax"][rez_type]
        rez_size_rbx = REGISTER_PREFIX_BY_LEN["rbx"][rez_type]
        op1_size = ""
        op2_size = ""

        if not self.var_op1.isnumeric():
            op1_index = self.var_positions[self.var_op1]
            var_type = self.var_types[self.var_op1]
            op1_size = REGISTER_PREFIX_BY_LEN["rax"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op1_size, "{} [rbp-{}]".format(var_type, str(op1_index))]))

        if not self.var_op2.isnumeric():
            op2_index = self.var_positions[self.var_op2]
            var_type = self.var_types[self.var_op2]
            op2_size = REGISTER_PREFIX_BY_LEN["rbx"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op2_size, "{} [rbp-{}]".format(var_type, str(op2_index))]))
        else:
            op2_size = int(self.var_op2)
        list_of_instr.append(instr_generator(OP_SUB, [op1_size, op2_size]))
        list_of_instr.append(instr_generator(OP_MOV, ["{} [rbp-{}]".format(rez_type, res_index), op1_size]))

        return list_of_instr

    def get_mul_instruction_asm(self):
        list_of_instr = []
        if self.var_op1.isnumeric() and self.var_op2.isnumeric():
            print("Cannot add 2 numerics. Only Variable and Variable or Variable and Number!")
            exit(1)
        if self.var_op1.isnumeric():
            print("First Operand Has to be a Variable!")
            exit(1)
        if self.var_rez.isnumeric():
            print("Result in ADD can't be a numeric!")
            exit(1)
        rez_type = self.var_types[self.var_rez]
        res_index = self.var_positions[self.var_rez]
        rez_size_rax = REGISTER_PREFIX_BY_LEN["rax"][rez_type]
        rez_size_rcx = REGISTER_PREFIX_BY_LEN["rcx"][rez_type]

        if not self.var_op1.isnumeric():
            op1_index = self.var_positions[self.var_op1]
            var_type = self.var_types[self.var_op1]
            op1_size = REGISTER_PREFIX_BY_LEN["rax"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op1_size, "{} [rbp-{}]".format(var_type, str(op1_index))]))

        if not self.var_op2.isnumeric():
            op2_index = self.var_positions[self.var_op2]
            var_type = self.var_types[self.var_op2]
            op2_size = REGISTER_PREFIX_BY_LEN["rcx"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op2_size, "{} [rbp-{}]".format(var_type, str(op2_index))]))
        else:
            op2_size = int(self.var_op2)
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [rez_size_rcx, op2_size]))

        list_of_instr.append(instr_generator(OP_MUL, [rez_size_rcx]))
        list_of_instr.append(instr_generator(OP_MOV, ["{} [rbp-{}]".format(rez_type, res_index), rez_size_rax]))

        return list_of_instr

    def get_div_instruction_asm(self):
        list_of_instr = []
        if self.var_op1.isnumeric() and self.var_op2.isnumeric():
            print("Cannot add 2 numerics. Only Variable and Variable or Variable and Number!")
            exit(1)
        if self.var_op1.isnumeric():
            print("First Operand Has to be a Variable!")
            exit(1)
        if self.var_rez.isnumeric():
            print("Result in ADD can't be a numeric!")
            exit(1)
        rez_type = self.var_types[self.var_rez]
        res_index = self.var_positions[self.var_rez]
        rez_size_rax = REGISTER_PREFIX_BY_LEN["rax"][rez_type]
        rez_size_rcx = REGISTER_PREFIX_BY_LEN["rcx"][rez_type]
        rez_size_rdx = REGISTER_PREFIX_BY_LEN["rdx"][rez_type]

        list_of_instr.append(instr_generator(OP_XOR, [rez_size_rdx, rez_size_rdx]))
        if not self.var_op1.isnumeric():
            op1_index = self.var_positions[self.var_op1]
            var_type = self.var_types[self.var_op1]
            op1_size = REGISTER_PREFIX_BY_LEN["rax"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op1_size, "{} [rbp-{}]".format(var_type, str(op1_index))]))

        if not self.var_op2.isnumeric():
            op2_index = self.var_positions[self.var_op2]
            var_type = self.var_types[self.var_op2]
            op2_size = REGISTER_PREFIX_BY_LEN["rcx"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op2_size, "{} [rbp-{}]".format(var_type, str(op2_index))]))
        else:
            op2_size = int(self.var_op2)
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [rez_size_rcx, op2_size]))

        list_of_instr.append(instr_generator(OP_DIV, [rez_size_rcx]))
        list_of_instr.append(instr_generator(OP_MOV, ["{} [rbp-{}]".format(rez_type, res_index), rez_size_rax]))

        return list_of_instr

    def get_eq_instruction_asm(self):
        list_of_instr = []
        rez_type = self.var_types[self.var_rez]
        res_index = self.var_positions[self.var_rez]
        rez_size_rax = REGISTER_PREFIX_BY_LEN["rax"][rez_type]
        op1_size = ""
        op2_size = ""
        if not self.var_op1.isnumeric():
            op1_index = self.var_positions[self.var_op1]
            var_type = self.var_types[self.var_op1]
            op1_size = REGISTER_PREFIX_BY_LEN["rax"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op1_size, "{} [rbp-{}]".format(var_type, str(op1_index))]))
        if not self.var_op2.isnumeric():
            op2_index = self.var_positions[self.var_op2]
            var_type = self.var_types[self.var_op2]
            op2_size = REGISTER_PREFIX_BY_LEN["rbx"][var_type]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 [op2_size, "{} [rbp-{}]".format(var_type, str(op2_index))]))

        list_of_instr.append(instr_generator(OP_CMP,
                                             [op1_size, op2_size]))
        list_of_instr.append(instr_generator(OP_SETE,
                                             ["al"]))
        list_of_instr.append(instr_generator(OP_MOV, ["{} [rbp-{}]".format(rez_type, res_index), "al"]))

        return list_of_instr

    def get_if_instruction_asm(self):
        list_of_instr = []
        if not self.var_op1.isnumeric():
            op1_index = self.var_positions[self.var_op1]
            var_type = self.var_types[self.var_op1]
            list_of_instr.append(instr_generator(OP_MOV,
                                                 ["al", "{} [rbp-{}]".format(var_type, str(op1_index))]))

        list_of_instr.append(instr_generator(OP_MOV, ["bl", "0"]))
        list_of_instr.append(instr_generator(OP_CMP, ["al", "bl"]))
        list_of_instr.append(instr_generator(OP_JE, ["ELSE_{}".format(self.if_count)]))
        # ist_of_instr.append(instr_generator(OP_CMP, ["al", "bl"]))
        # AICI AL AR TREBUI SA FIE 0 ca sa fie TRUE
        self.if_start = True

        return list_of_instr

    def get_else_instruction_asm(self):
        list_of_instr = []
        if not self.else_start or not self.if_start:
            print("Something went wrong in the if-else!")
            exit(1)
        list_of_instr.append(instr_generator(OP_JMP, ["ENDIF_{}".format(self.if_count)]))
        list_of_instr.append(instr_generator(OP_LABEL, ["ELSE_{}".format(self.if_count)]))
        return list_of_instr

    def get_endif_instruction_asm(self):
        list_of_instr = []
        if not self.else_start or not self.if_start or not self.endif_found:
            print("Something went wrong in the if-else!")
            exit(1)
        list_of_instr.append(instr_generator(OP_LABEL, ["ENDIF_{}".format(self.if_count)]))
        self.if_count += 1
        self.if_start = False
        self.else_start = False
        self.endif_found = False
        return list_of_instr

    def generate_asm_from_line(self):
        list_of_instr = []

        if self.state == "VARIABLE":
            list_of_instr.extend(self.get_variable_instruction_asm())
        elif self.state == "CALL":
            list_of_instr.extend(self.get_call_instruction_asm())
        elif self.state == "ADD":
            list_of_instr.extend(self.get_add_instruction_asm())
        elif self.state == "SUB":
            list_of_instr.extend(self.get_sub_instruction_asm())
        elif self.state == "MUL":
            list_of_instr.extend(self.get_mul_instruction_asm())
        elif self.state == "DIV":
            list_of_instr.extend(self.get_div_instruction_asm())
        elif self.state == "EQ":
            list_of_instr.extend(self.get_eq_instruction_asm())
        elif self.state == "IF":
            list_of_instr.extend(self.get_if_instruction_asm())
        elif self.state == "ELSE":
            list_of_instr.extend(self.get_else_instruction_asm())
        elif self.state == "ENDIF":
            list_of_instr.extend(self.get_endif_instruction_asm())

        return list_of_instr

    def reset(self):
        self.line = ""
        self.state = None
        self.var_name = None
        self.var_value = 0
        self.var_size = 0
        self.var_type = None
        self.func_name = None
        self.func_with_var = False
        self.var_rez = ""
        self.var_op1 = ""
        self.var_op2 = ""

    def interpret_line(self, line):
        self.reset()
        self.line = line
        split_line = self.line.split(" ")
        for idx, word in enumerate(split_line):
            self.check_word(word.strip(), idx)

        return self.generate_asm_from_line()

    def check_word(self, word, idx):
        if word not in SYNTAX_RULES_INDEX.keys():
            if self.state == "VARIABLE":
                self.set_data_for_variable(word, idx)
            elif self.state == "CALL":
                self.set_data_for_call(word, idx)
            elif self.state == "ADD":
                self.set_data_for_add(word, idx)
            elif self.state == "SUB":
                self.set_data_for_sub(word, idx)
            elif self.state == "MUL":
                self.set_data_for_mul(word, idx)
            elif self.state == "DIV":
                self.set_data_for_div(word, idx)
            elif self.state == "EQ":
                self.set_data_for_eq(word, idx)
            elif self.state == "IF":
                self.set_data_for_if(word, idx)
            return
        if idx != SYNTAX_RULES_INDEX[word]:
            print("Word {} not in the right index {} - but should be {}". format(word, idx, SYNTAX_RULES_INDEX[word]))
            exit(1)
        self.state = SYNTAX_RULES_TYPE[word]
        if self.state == "VARIABLE":
            self.var_size = DATA_TYPE_SIZES[word]
            self.var_type = word
        elif self.state == "CALL":
            return
        elif self.state == "ADD":
            return
        elif self.state == "SUB":
            return
        elif self.state == "MUL":
            return
        elif self.state == "DIV":
            return
        elif self.state == "EQ":
            return
        elif self.state == "IF":
            self.if_start = True
            return
        elif self.state == "ELSE":
            self.else_start = True
            return
        elif self.state == "ENDIF":
            self.endif_found = True
            return

    def set_data_for_if(self, word, idx):
        if idx == 1:
            self.var_op1 = word

    def set_data_for_eq(self, word, idx):
        if idx == 1:
            self.var_rez = word
        if idx == 2 and word == "=":
            return
        if idx == 3:
            self.var_op1 = word
        if idx == 4 and word == "==":
            return
        if idx == 5:
            self.var_op2 = word

    def set_data_for_variable(self, word, idx):
        if idx == 1:
            self.var_name = word
            if self.var_name in self.var_positions:
                print("Variable {} already declared!".format(self.var_name))
                exit(1)
            self.var_positions[self.var_name] = None
        elif idx == 2 and word == "=":
            return
        elif idx == 3:
            self.var_value = int(word)
            self.var_positions[self.var_name] = self.depth_rsp_func + DATA_TYPE_SIZES[self.var_type]
            self.var_types[self.var_name] = self.var_type

    def set_data_for_call(self, word, idx):
        if idx == 1:
            self.func_name = word
        if idx == 2:
            if word.isnumeric():
                self.var_value = int(word)
            elif word in self.var_positions.keys():
                self.func_with_var = True
                self.var_name = word

    def set_data_for_add(self, word, idx):
        if idx == 1:
            self.var_rez = word
        elif idx == 2 and word == "=":
            return
        elif idx == 3:
            self.var_op1 = word
        elif idx == 4 and word == "+":
            return
        elif idx == 5:
            self.var_op2 = word

    def set_data_for_sub(self, word, idx):
        if idx == 1:
            self.var_rez = word
        elif idx == 2 and word == "=":
            return
        elif idx == 3:
            self.var_op1 = word
        elif idx == 4 and word == "-":
            return
        elif idx == 5:
            self.var_op2 = word

    def set_data_for_mul(self, word, idx):
        if idx == 1:
            self.var_rez = word
        elif idx == 2 and word == "=":
            return
        elif idx == 3:
            self.var_op1 = word
        elif idx == 4 and word == "*":
            return
        elif idx == 5:
            self.var_op2 = word

    def set_data_for_div(self, word, idx):
        if idx == 1:
            self.var_rez = word
        elif idx == 2 and word == "=":
            return
        elif idx == 3:
            self.var_op1 = word
        elif idx == 4 and word == "/":
            return
        elif idx == 5:
            self.var_op2 = word
