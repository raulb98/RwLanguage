# RwLanguage
RwLanguage written in Python.
The end phase of the project will be to use RW to generate the compiler and stop depending on Python for this process.

## Usage

```
usage: main.py [-h] [-asm ASM_FILE] [-out EXE_FILE] [-int INTERPRET] [-gen GENERATE]

RW compiler 1.0

options:
  -h, --help            show this help message and exit
  -asm ASM_FILE, --asm_file ASM_FILE
                        The path to the .asm input file
  -out EXE_FILE, --exe_file EXE_FILE
                        The path to the .exe output file
  -int INTERPRET, --interpret INTERPRET
                        The path to the .rw file to interpret
  -gen GENERATE, --generate GENERATE
                        Generate .asm from interpreted code
```

### Explanation
The python script will compile the RW instructions and it will generate the assembly which can generate the object files.
From here the compiling is simple. The compiler will generate the .obj file with `nasm` which will further be used to generate the executable with Microsoft Compiler `cl`.

### TODO
1. Implement nested IF instructions.
2. Implement more boolean operations.
3. Implement iterative process (FOR, WHILE).
