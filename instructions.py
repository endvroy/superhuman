# define instructions used in Human Resource Machine Game
from state import State
from state import Cell
from enum import Enum
import copy


def add(st, loc):
    if st.reg.val is None:
        raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem) or st.mem[loc].val is None:
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.reg = newSt.reg + newSt.mem[loc]
    return newSt


def sub(st, loc):
    if st.reg is None or st.mem[loc].val is None:
        raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem):
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.reg = newSt.reg - newSt.mem[loc]
    return newSt


def copyFrom(st, loc):
    if 0 > loc > len(st.mem) or st.mem[loc].val is None:
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.reg.copyFrom(newSt.mem[loc])
    return newSt


def copyTo(st, loc):
    if st.reg is None:
        raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem):
        raise ValueError('invalid mem write at loc: ' + str(loc))
    newSt = State(st=st)
    newSt.mem[loc].copyFrom(newSt.reg)
    return newSt


def inbox(st):
    if not st.input:
        raise ValueError('invalid inbox on empty input')
    return State(st.input[1:], Cell(st.input[0]), st.mem, st.output)


def outbox(st):
    if st.reg is None:
        raise ValueError('invalid read on null reg')
    newSt = State(st=st)
    newSt.output += (st.reg.val,)
    newSt.reg.used = True
    return newSt


if __name__ == '__main__':
    st = State((1,), Cell(None), Cell.cell_array([2, None, 4]), ())
    print(st)
    st = inbox(st)
    print(st)
    st = add(st, 0)
    print(st)
    st = copyFrom(st, 0)
    print(st)
    st = copyTo(st, 0)
    print(st)
    st = sub(st, 0)
    print(st)
    st = outbox(st)
    print(st)
