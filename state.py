class State:
    """State defines a state of the Human Resource Machine"""

    def __init__(self, mem=None, output=None):
        if mem is None:
            mem = []
        if output is None:
            output = []
        self.mem = list(mem)
        self.output = list(output)

    def copy(self):
        return State(self.mem, self.output)

    def __str__(self):
        # return str(self.reg) + ' ' + str(self.mem) + ' ' + str(self.output)
        return "state{" + str(self.mem) + ', ' + str(self.output) + "}"

    def __repr__(self):
        return str(self)
