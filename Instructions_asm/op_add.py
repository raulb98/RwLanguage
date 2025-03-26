import instruction


class ADD(instruction.Instruction):
    def __init__(self, op_code, args):
        super().__init__(op_code, args)

    def execute(self, fwrite):
        fwrite.write("\t\tadd {}, {}".format(self.args[0], self.args[1]))
        fwrite.write("\n")
