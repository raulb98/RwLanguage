import os
import subprocess
import argparse
import sys
sys.path.append(os.path.join(os.getcwd(), "Instructions_asm"))
sys.path.append(os.path.join(os.getcwd(), "interpretor"))
from Instructions_asm.instr_opcodes import *
from interpretor.reader import *
from Instructions_asm.instr_generator import instr_generator


print_nr_asm = """
section .data
    buffer db 20 dup(0)          ; Buffer to store the string
    buffer_len equ $ - buffer    ; Buffer length
    newline db 13, 10, 0         ; Newline (CRLF)

section .bss
    hStdOut resq 1               ; Handle for stdout

section .text
    global main
    extern GetStdHandle, WriteConsoleA, ExitProcess

    ; Function: print_number
    ; Parameter: rcx (number to print)
"""

TEXT_SECTION = """
section .text
    global main
    extern GetStdHandle, WriteConsoleA, ExitProcess
"""

BSS_SECTION = """
section .bss
    hStdOut resq 1               ; Handle for stdout
"""

DATA_SECTION = """
section .data
    buffer db 20 dup(0)          ; Buffer to store the string
    buffer_len equ $ - buffer    ; Buffer length
    newline db 13, 10, 0         ; Newline (CRLF)
"""

PRINT_NR = """
print_number:
    push rbp
    mov rbp, rsp
    sub rsp, 40                 ; Allocate shadow space

    mov rdi, buffer + buffer_len ; Point to the end of buffer
    mov rbx, 10                 ; Base 10 divisor
    mov rax, [rbp+16]            ; Load number
    mov rcx, 0                  ; Digit count

    test rax, rax
    jns convert_loop            ; If number is positive, skip negation
    neg rax                     ; Convert negative to positive

convert_loop:
    xor rdx, rdx
    div rbx                     ; RAX / 10, remainder in RDX
    add dl, '0'                 ; Convert to ASCII
    dec rdi                     ; Move buffer pointer back
    mov [rdi], dl               ; Store character
    inc rcx                     ; Increase count
    test rax, rax
    jnz convert_loop

    ; Handle negative sign
    cmp rcx, 0
    jz skip_sign
    test rcx, rcx
    jns skip_sign
    dec rdi
    mov byte [rdi], '-'

skip_sign:
    ; Get handle to stdout
    sub rsp, 28h
    mov ecx, -11
    call GetStdHandle
    mov [hStdOut], rax

    ; Write number to console
    mov rcx, [hStdOut]
    mov rdx, rdi
    mov rax, 0
    add rax, buffer
    add rax, buffer_len
    sub rax, rdi
    mov r8, rax
    lea r9, [rsp+20h]
    mov qword [rsp+28h], 0
    call WriteConsoleA

    ; Print newline
    mov rcx, [hStdOut]
    mov rdx, newline
    mov r8, 2
    lea r9, [rsp+20h]
    mov qword [rsp+28h], 0
    call WriteConsoleA

    add rsp, 28h
    leave
    ret
"""


def generate_req_asm(asm_file_handle):
    asm_file_handle.write(DATA_SECTION)
    asm_file_handle.write("\n")
    asm_file_handle.write(BSS_SECTION)
    asm_file_handle.write("\n")
    asm_file_handle.write(TEXT_SECTION)
    asm_file_handle.write("\n")
    asm_file_handle.write(PRINT_NR)
    asm_file_handle.write("\n")
    asm_file_handle.write("\n")
    asm_file_handle.write("main:\n")


def compile_asm(asm_file):
    obj_file = ""
    if asm_file.endswith(".asm"):
        obj_file = asm_file.replace(".asm", ".obj")
    else:
        obj_file = "prog.obj"
    subprocess.Popen(['nasm', '-f', 'win64', asm_file, '-o', obj_file], shell=False)
    subprocess.Popen(['cl', obj_file, 'kernel32.lib', 'ntdll.lib', '/link', '/SUBSYSTEM:CONSOLE', '/entry:main',
                      '/LARGEADDRESSAWARE:NO'], shell=False)


def interpret_rw(rw_file):
    rw_file_handle = open(rw_file, "r")
    asm_file_handle = open("rw_test.asm", "w")
    reader = Reader()
    list_of_instructions = [
        instr_generator(OP_PUSH, ["rbp"]),
        instr_generator(OP_MOV, ["rbp", "rsp"]),
    ]
    for line in rw_file_handle:
        if len(line) == 0:
            continue
        line = line.strip()
        new_instr = reader.interpret_line(line)
        list_of_instructions.extend(new_instr)

    generate_req_asm(asm_file_handle)
    list_of_instructions.append(instr_generator(OP_ADD, ["rsp", str(reader.depth_rsp_func)]))
    list_of_instructions.append(instr_generator(OP_POP, ["rbp"]))
    list_of_instructions.append(instr_generator(OP_RET, []))
    for instruction in list_of_instructions:
        instruction.execute(asm_file_handle)

    rw_file_handle.close()
    asm_file_handle.close()


def generate_asm_test(asm_file_generate_name):
    asm_file_handle = open(asm_file_generate_name, "w")
    asm_file_handle.write(DATA_SECTION)
    asm_file_handle.write("\n")
    asm_file_handle.write(BSS_SECTION)
    asm_file_handle.write("\n")
    asm_file_handle.write(TEXT_SECTION)
    asm_file_handle.write("\n")
    asm_file_handle.write(PRINT_NR)
    asm_file_handle.write("\n")
    asm_file_handle.write("\n")
    asm_file_handle.write("main:\n")

    instructions = [
                    instr_generator(OP_XOR, ["rcx", "rcx"]),
                    instr_generator(OP_ADD, ["rcx", 2]),
                    instr_generator(OP_ADD, ["rcx", 2]),
                    instr_generator(OP_ADD, ["rcx", 2]),

                    instr_generator(OP_PUSH, ["rcx"]),
                    instr_generator(OP_CALL, ["print_number"]),
                    instr_generator(OP_POP, ["rcx"]),

                    instr_generator(OP_XOR, ["rcx", "rcx"]),

                    instr_generator(OP_PUSH, ["rcx"]),
                    instr_generator(OP_CALL, ["print_number"]),
                    instr_generator(OP_POP, ["rcx"])

                    ]

    for instruction in instructions:
        instruction.execute(asm_file_handle)

    asm_file_handle.close()


def main():
    parser = argparse.ArgumentParser(description="RW compiler 1.0")
    parser.add_argument("-asm", "--asm_file", type=str, help="The path to the .asm input file")
    parser.add_argument("-out", "--exe_file", type=str, help="The path to the .exe output file")
    parser.add_argument("-int", "--interpret", type=str, help="The path to the .rw file to interpret")
    parser.add_argument("-gen", "--generate", type=str, help="Generate .asm from interpreted code")

    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.generate:
        generate_asm_test(args.generate)
        compile_asm(args.generate)

    if args.interpret and args.asm_file:
        interpret_rw(args.interpret)
        compile_asm(args.asm_file)


if __name__ == "__main__":
    main()