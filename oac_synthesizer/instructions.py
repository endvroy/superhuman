# define instructions used in Human Resource Machine Game
from enum import Enum
from state import State, Cell


def add(st, loc):
    if st.reg.is_empty():
        raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem) or st.mem[loc].is_empty():
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.reg = newSt.reg + newSt.mem[loc]
    return newSt


def sub(st, loc):
    if st.reg.is_empty():
        raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem) or st.mem[loc].is_empty():
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.reg = newSt.reg - newSt.mem[loc]
    return newSt


def copyFrom(st, loc):
    if 0 > loc > len(st.mem) or st.mem[loc].is_empty():
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.reg.copyFrom(newSt.mem[loc])
    return newSt


def copyTo(st, loc):
    if st.reg.is_empty():
        raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem):
        raise ValueError('invalid mem write at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.mem[loc].copyFrom(newSt.reg)
    return newSt


def inbox(st):
    if not st.input:
        raise ValueError('invalid inbox on empty input')
    newSt = State(st=st)
    newSt.input, newSt.reg = st.input[1:], Cell(st.input[0])
    return newSt


def outbox(st):
    if st.reg.is_empty():
        raise ValueError('invalid read on null reg')
    newSt = State(st=st)
    newSt.output += (st.reg.val,)
    newSt.reg.value = None
    newSt.reg.used = False
    return newSt


# jump instructions used in the synthesizer
# h is the history
# i is the index of inst in the history where jump occurs
def jump(st, i):
    return State(st=st)


def jumpIfZero(st, i):
    if st.reg.is_empty():
        raise ValueError('invalid read on null reg')
    return State(st=st)


def jumpIfNegative(st, i):
    if st.reg.is_empty():
        raise ValueError('invalid read on null reg')
    return State(st=st)

def jumpFrom(st, i):
    return State(st=st)

def jumpIfZeroFrom(st, i):
    return State(st=st)

def jumpIfNegativeFrom(st, i):
    return State(st=st)
