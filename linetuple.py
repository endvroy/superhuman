from state import State
from enum import Enum
import instructions as op


class LineTuple:
    # A LineTuple object represents a line of code
    # A LineTuple should be like "operator op1 op2 op3"
    # op1 = CopyFrom, op2 = loc op3 = CopyTo
    def __init__(self, operator=None, state=None, copyFrom=0, loc=-1, copyTo=-1):
        if operator is None or state is None:
            raise ValueError('Empty operator or state')
        self.hasNext = False
        self.operator = operator
        self.copyFrom = copyFrom
        self.loc = loc
        self.copyTo = copyTo
        # Calculate the new state
        if operator == "add":
            self.state = op.add(state, copyFrom, loc, copyTo)
        elif operator == "sub":
            self.state = op.sub(state, copyFrom, loc, copyTo)
        elif operator == "outbox":
            self.state = op.outbox(state, copyFrom)
        else:
            raise ValueError("Invalid operator: " + operator)

    def getState(self):
        return self.state

    def getInstWithArgs(self):
        if self.operator == "add":
            return op.add, [self.copyFrom, self.loc, self.copyTo]
        elif self.operator == "sub":
            return op.sub, [self.copyFrom, self.loc, self.copyTo]
        elif self.operator == "outbox":
            return op.outbox, [self.copyFrom]
        else:
            raise ValueError("Invalid operator: " + self.operator)

    def __str__(self):
        # return str(self.reg) + ' ' + str(self.mem) + ' ' + str(self.output)
        if self.operator is not "outbox":
            return str(self.hasNext) + ' ' + self.operator + ' ' + str(self.copyFrom) + ' ' + str(self.loc) + ' ' + str(
                self.copyTo) + ' ' + str(self.state)
        else:
            return str(self.hasNext) + ' ' + self.operator + ' ' + str(self.copyFrom) + ' ' + str(self.state)

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    st = State([2, 3, 4], [])
    print(st)
    line1 = LineTuple("add", st, 0, 2, 1)
    st = line1.getState()
    print(st)
    line2 = LineTuple("sub", st, 0, 1, 2)
    st = line2.getState()
    print(st)
    line3 = LineTuple("outbox", st, loc=2)
    st = line3.getState()
    print(st)
    line4 = LineTuple("outbox", st, loc=1)
    st = line4.getState()
    print(st)
    line5 = LineTuple("outbox", st, loc=0)
    st = line5.getState()
    print(st)
