import instruction


class JE(instruction.Instruction):
    def __init__(self, op_code, args):
        super().__init__(op_code, args)

    def execute(self, fwrite):
        fwrite.write("\t\tje {}".format(self.args[0]))
        fwrite.write("\n")
