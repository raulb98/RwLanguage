class Instruction:
    def __init__(self, op_code, args):
        self.op_code = op_code
        self.args = args

    def execute(self, fwrite):
        pass
