import instruction


class RET(instruction.Instruction):
    def __init__(self, op_code, args):
        super().__init__(op_code, args)

    def execute(self, fwrite):
        fwrite.write("\t\tret")
        fwrite.write("\n")
