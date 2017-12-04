# define instructions used in Human Resource Machine Game
from state import State
from enum import Enum


def add(st, copyFrom, loc, copyTo):
    # if st.reg is None:
    #     raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem) or loc < 0 or st.mem[loc] is None:
        raise ValueError('invalid mem read at loc: ' + str(loc))
    if 0 > copyFrom > len(st.mem) or st.mem[copyFrom] is None:
        raise ValueError('invalid mem read at loc: ' + str(loc))
    if 0 > copyTo > len(st.mem):
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newMem = st.mem.copy()
    newMem[copyTo] = newMem[copyFrom] + newMem[loc]
    return State(mem=newMem, output=st.output)


def sub(st, copyFrom, loc, copyTo):
    # if st.reg is None:
    #     raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem) or loc < 0 or st.mem[loc] is None:
        raise ValueError('invalid mem read at loc: ' + str(loc))
    if 0 > copyFrom > len(st.mem) or st.mem[copyFrom] is None:
        raise ValueError('invalid mem read at loc: ' + str(loc))
    if 0 > copyTo > len(st.mem):
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newMem = st.mem.copy()
    newMem[copyTo] = newMem[copyFrom] - newMem[loc]
    return State(mem=newMem, output=st.output)


# def copyFrom(st, loc):
#     if 0 > loc > len(st.mem):
#         raise ValueError('invalid mem read at loc: ' + str(loc))
#     newSt = State(st)
#     newSt.reg = newSt.mem[loc]
#     return newSt

# def copyTo(st, loc):
#     if st.reg is None:
#         raise ValueError('invalid read on null reg')
#     if 0 > loc > len(st.mem):
#         raise ValueError('invalid mem write at loc: ' + str(loc))
#     newSt = State(st)
#     newSt.mem[loc] = newSt.reg
#     return newSt

def outbox(st, loc):
    # if st.reg is None:
    #     raise ValueError('invalid read on null reg')
    if 0 > loc > len(st.mem) or st.mem[loc] == None:
        raise ValueError('invalid mem read at loc: ' + str(loc))
    newSt = st.copy()
    newSt.output.append(st.mem[loc])
    return newSt

def inbox(st, loc):
    if 0 > loc > len(st.mem):
        raise ValueError('invalid mem read at loc: ' + str(loc))
    if len(st.input) <= 0:
        raise ValueError('Inbox empty')
    newSt = st.copy()
    newSt.mem[loc] = newSt.input.pop(0)
    return newSt


# class ArgType(object):
#     def __init__(self, useReg=False, argList=[]):
#         self.useReg = useReg
#         self.argList = argList
#     def __str__(self):
#         return '(' + str(self.useReg) + ' ' + str(self.argList) +')'
#     def __repr__(self):
#         return str(self)


# instArgsMap = {
#     add : ArgType(True, ['l']),
#     sub : ArgType(True, ['l']),
#     copyFrom : ArgType(False, ['l']),
#     copyTo : ArgType(True, ['l']),
#     outbox : ArgType(True, [])
# }


if __name__ == '__main__':
    st = State([1,2,3], [None, None, None], [])
    print(st)
    st = inbox(st, 0)
    print(st)
    st = outbox(st, 0)
    print(st)
    st = inbox(st, 0)
    print(st)
    st = outbox(st, 0)
    print(st)
    st = inbox(st, 0)
    print(st)
    st = outbox(st, 0)
    print(st)
