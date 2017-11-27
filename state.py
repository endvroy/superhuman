from copy import deepcopy


class State(object):
    """State defines a state of the Human Resource Machine"""

    def __init__(self, st=None, mem=None, output=None):
        if output is None:
            output = []
        if mem is None:
            mem = []
        if st:
            # self.reg = st.reg
            self.mem = deepcopy(st.mem)
            self.output = deepcopy(st.output)
        else:
            # self.reg = reg
            self.mem = mem
            self.output = output

    def __str__(self):
        # return str(self.reg) + ' ' + str(self.mem) + ' ' + str(self.output)
        return "state{" + str(self.mem) + ', ' + str(self.output) + "}"

    def __repr__(self):
        return str(self)
