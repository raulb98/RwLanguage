import instruction


class JNE(instruction.Instruction):
    def __init__(self, op_code, args):
        super().__init__(op_code, args)

    def execute(self, fwrite):
        fwrite.write("\t\tjne {}".format(self.args[0]))
        fwrite.write("\n")
