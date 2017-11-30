from collections import namedtuple

class Cell(object):
    def __init__(self, val, used=False):
        self.val = val
        self.used = used

    def copyFrom(self, other):
        # copy from other cell
        other.used = True
        self.used = False
        self.val = other.val

    def is_empty(self):
        return self.val is None

    # operators
    def __add__(self, other):
        self.used = True
        other.used = True
        return Cell(self.val+other.val)

    def __radd__(self, other):
        return self.val == other

    def __sub__(self, other):
        self.used = True
        other.used = True
        return Cell(self.val-other.val)

    def __eq__(self, other):
        return self.val == other.val

    def __hash__(self):
        return hash((self.val, self.used))

    # helper methods
    @staticmethod
    def cell_array(a, used=False):
        return tuple([Cell(v, used) for v in a])

    @staticmethod
    def copy(c):
        return Cell(c.val, c.used)

    def __str__(self):
        # used is red, unused is green
        color = "\033[1;31m" if self.used else "\033[0;32m"
        return color + str(self.val) + "\033[0m"

    def __repr__(self):
        return str(self)

class State(object):
    """State defines a state of the Human Resource Machine"""
    def __init__(self, Input=None, reg=None, mem=None, output=None, st=None):
        if st:
            self.reg = Cell.copy(st.reg)
            self.mem = tuple(map(Cell.copy, st.mem))
            self.input = st.input
            self.output = st.output
        else:
            self.reg = Cell(reg)
            self.mem = Cell.cell_array(mem)
            self.input = Input
            self.output = output

    def __hash__(self):
        return hash((self.input, self.reg, self.mem, self.output))

    def __eq__(self, other):
        return self.reg == other.reg and self.input == other.input \
            and self.mem == other.mem and self.output == other.output

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return str(self.input) + ' ' + str(self.reg) + ' ' + str(self.mem) + ' ' + str(self.output)

    def __repr__(self):
        return str(self)
