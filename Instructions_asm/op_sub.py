import instruction


class SUB(instruction.Instruction):
    def __init__(self, op_code, args):
        super().__init__(op_code, args)

    def execute(self, fwrite):
        fwrite.write("\t\tsub {}, {}".format(self.args[0], self.args[1]))
        fwrite.write("\n")
