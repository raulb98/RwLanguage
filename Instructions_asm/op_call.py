import instruction


class CALL(instruction.Instruction):
    def __init__(self, op_code, args):
        super().__init__(op_code, args)

    def execute(self, fwrite):
        fwrite.write("\t\tcall {}".format(self.args[0]))
        fwrite.write("\n")
