# define instructions used in Human Resource Machine Game
from state import State
from enum import Enum
import copy

def add(st, loc):
    if st.reg is None:
        raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem):
        raise ValueError('invalid mem read at loc: ' + str(loc))
    return State(st.reg+st.mem[loc], copy.deepcopy(st.mem), copy.deepcopy(st.output))

def sub(st, loc):
    if st.reg is None:
        raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem):
        raise ValueError('invalid mem read at loc: ' + str(loc))
    return State(st.reg-st.mem[loc], copy.deepcopy(st.mem), copy.deepcopy(st.output))

def copyFrom(st, loc):
    if 0 > loc > len(st.mem):
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.reg = newSt.mem[loc]
    return newSt

def copyTo(st, loc):
    if st.reg is None:
        raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem):
        raise ValueError('invalid mem write at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.mem[loc] = newSt.reg
    return newSt

def outbox(st):
    if st.reg is None:
        raise ValueError('invalid read on null reg')
    newSt = State(st=st)
    newSt.output.append(st.reg)
    return newSt

class ArgType(object):
    def __init__(self, useReg=False, argList=[]):
        self.useReg = useReg
        self.argList = argList
    def __str__(self):
        return '(' + str(self.useReg) + ' ' + str(self.argList) +')'
    def __repr__(self):
        return str(self)


instArgsMap = {
    add : ArgType(True, ['l']),
    sub : ArgType(True, ['l']),
    copyFrom : ArgType(False, ['l']),
    copyTo : ArgType(True, ['l']),
    outbox : ArgType(True, [])
}


if __name__ == '__main__':
    st = State(1, [2, 3, 4], [])
    print st
    st = add(st, 0)
    print st
    st = copyFrom(st, 0)
    print st
    st = sub(st, 0)
    print st
    st = outbox(st)
    print st
