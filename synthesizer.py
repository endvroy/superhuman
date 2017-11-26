import instructions
import itertools
from collections import namedtuple
from collections import defaultdict

from state import State
from linetuple import LineTuple

beamState = namedtuple("beamState", "lineInst, backptr, score")

def scoreInstruction(state, target):
    # Linear combination of 
    return []

def enumerateInstruction(state, instructions, lastLine, target):
    lineInsts = []
    if state.mem is not None:
        validMemIndex = []
        for i in range(len(state.mem)):
            if state.mem[i] is not None:
                validMemIndex.append(i)
                lineInsts.append(LineTuple("outbox", state, loc=i))
        rawLineInsts = list(itertools.product(instructions, validMemIndex, validMemIndex, range(len(state.mem))))
        for line in rawLineInsts:
            lineInsts.append(LineTuple(line[0], state, line[1], line[2], line[3]))
    stateTupleList = []
    for inst in lineInsts:
        stateTupleList.append(beamState(inst, lastLine, scoreInstruction(inst, target)))


def enumerateNextInstruction(line, instructions, target):
    state = line.state
    return enumerateInstruction(state, instructions, line, target)

def pruneStack(stack):
    return []

def beam(beginst, lineLimit, pruneLimit):
    # Key: current 
    stacks = [[] for _ in range(lineLimit+1)]




if __name__ == '__main__':
    st = State(None, [2, None, 3], [])
    # instSet = [instructions.add, instructions.sub, instructions.outbox]
    instSet = ["add", "sub"]
    result = enumerateInstruction(st, instSet)
    for entry in result:
        print entry
    # print enumerateInsts(st, instSet, 2)
