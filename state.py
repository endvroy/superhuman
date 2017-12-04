class State:
    """State defines a state of the Human Resource Machine"""

    def __init__(self, inputs=None, mem=None, output=None):
        if inputs is None:
            inputs = []
        if mem is None:
            mem = []
        if output is None:
            output = []
        self.input = list(inputs)
        self.mem = list(mem)
        self.output = list(output)

    def copy(self):
        return State(self.input, self.mem, self.output)

    def __eq__(self, other):
        if self.input == other.input and self.mem == other.mem and self.output == other.output:
            return True
        else:
            return False

    def __str__(self):
        # return str(self.reg) + ' ' + str(self.mem) + ' ' + str(self.output)
        return "state{" + str(self.input) + ', ' + str(self.mem) + ', ' + str(self.output) + "}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((tuple(self.input), tuple(self.mem), tuple(self.output)))
