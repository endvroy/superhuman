from copy import deepcopy
from collections import namedtuple

class Cell(object):
    def __init__(self, val, used=False):
        self.val = val
        self.used = used

    @staticmethod
    def copyFrom(c):
        # copy from other cell
        c.used = True
        return Cell(c.val)

    # operators
    def __add__(self, other):
        self.used = True
        other.used = True
        return Cell(self.val+other.val)

    def __sub__(self, other):
        self.used = True
        other.used = True
        return Cell(self.val-other.val)

    # helper methods
    @staticmethod
    def cell_array(a, used=False):
        return [Cell(v, used) for v in a]

    @staticmethod
    def copy(c):
        if not c:
            return None
        return Cell(c.val, c.used)

    def __str__(self):
        # used is red, unused is green
        color = "\033[1;31m" if self.used else "\033[0;32m"
        return color + str(self.val) + "\033[0m"

    def __repr__(self):
        return str(self)


class State(object):
    """State defines a state of the Human Resource Machine"""
    def __init__(self, input=None, reg=None, mem=None, output=None, st=None):
        if st:
            self.reg = Cell.copy(st.reg)
            self.input = deepcopy(input)
            self.mem = deepcopy(st.mem)
            self.output = deepcopy(st.output)
        else:
            self.reg = Cell.copy(reg)
            self.input = deepcopy(input)
            self.mem = deepcopy(mem)
            self.output = deepcopy(output)

    def __str__(self):
        return str(self.input) + ' ' + str(self.reg) + ' ' + str(self.mem) + ' ' + str(self.output)

    def __repr__(self):
        return str(self)
