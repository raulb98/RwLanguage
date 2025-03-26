from instr_opcodes import *
import op_add
import op_call
import op_xor
import op_sub
import op_push
import op_pop
import op_mov
import op_mul
import op_div
import op_cmp
import op_sete
import op_ret
import op_je
import op_jne
import op_label
import op_jmp

def instr_generator(op_code, args):
    if op_code == OP_ADD:
        return op_add.ADD(op_code, args)
    elif op_code == OP_CALL:
        return op_call.CALL(op_code, args)
    elif op_code == OP_XOR:
        return op_xor.XOR(op_code, args)
    elif op_code == OP_SUB:
        return op_sub.SUB(op_code, args)
    elif op_code == OP_PUSH:
        return op_push.PUSH(op_code, args)
    elif op_code == OP_POP:
        return op_pop.POP(op_code, args)
    elif op_code == OP_MOV:
        return op_mov.MOV(op_code, args)
    elif op_code == OP_MUL:
        return op_mul.MUL(op_code, args)
    elif op_code == OP_DIV:
        return op_div.DIV(op_code, args)
    elif op_code == OP_CMP:
        return op_cmp.CMP(op_code, args)
    elif op_code == OP_SETE:
        return op_sete.SETE(op_code, args)
    elif op_code == OP_RET:
        return op_ret.RET(op_code, args)
    elif op_code == OP_JE:
        return op_je.JE(op_code, args)
    elif op_code == OP_JNE:
        return op_jne.JNE(op_code, args)
    elif op_code == OP_LABEL:
        return op_label.LABEL(op_code, args)
    elif op_code == OP_JMP:
        return op_jmp.JMP(op_code, args)
