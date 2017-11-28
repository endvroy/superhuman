class State:
    """State defines a state of the Human Resource Machine"""

    def __init__(self, mem=None, output=None):
        if output is None:
            output = []
        if mem is None:
            mem = []
        self.mem = mem
        self.output = output

    def copy(self):
        return State(self.mem.copy(), self.output.copy())

    def __repr__(self):
        return 'State(mem={}, output={})'.format(self.mem, self.output)
