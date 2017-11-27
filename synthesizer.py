import itertools
import os
from collections import namedtuple

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
    stateTuples = {"outbox": [], "arith": []}
    for inst in lineInsts:
        if inst.operator == "outbox":
            stateTuples["outbox"].append(beamState(inst, lastLine, scoreInstruction(inst, target)))
        else:
            stateTuples["arith"].append(beamState(inst, lastLine, scoreInstruction(inst, target)))
    return stateTuples


def enumerateNextInstruction(beamstate, instructions, target):
    line = beamstate.lineInst
    state = line.state
    return enumerateInstruction(state, instructions, beamstate, target)


def pruneStack(stack, target):
    # outbox
    for statetuple in stack["outbox"][:]:
        line = statetuple.lineInst
        state = line.state
        output = state.output
        commonPrefix = os.path.commonprefix([line.state.output, target])
        if len(commonPrefix) < len(output) or len(output) > len(target):
            stack["outbox"].remove(statetuple)
            # arithmetic


def printStack(stack):
    for state in stack["outbox"]:
        print('-', state)
    for state in stack["arith"]:
        print('-', state)
    print('\n')


def beam(beginst, instSet, target, lineLimit, pruneLimit):
    # Key: current 
    stacks = [{"outbox": [], "arith": []} for _ in range(lineLimit + 1)]

    enumInst = enumerateInstruction(beginst, instSet, None, target)
    stacks[0]["outbox"] = enumInst["outbox"]
    stacks[0]["arith"] = enumInst["arith"]

    print("stack 0:")
    pruneStack(stacks[0], target)
    printStack(stacks[0])

    for i in range(lineLimit):
        i = i + 1
        print("stack " + str(i) + " :")
        for state in stacks[i - 1]["outbox"] + stacks[i - 1]["arith"]:
            enumInst = enumerateNextInstruction(state, instSet, target)
            stacks[i]["outbox"] += enumInst["outbox"]
            stacks[i]["arith"] += enumInst["arith"]
        pruneStack(stacks[i], target)
        printStack(stacks[i])


if __name__ == '__main__':
    st = State(None, [2, None, 3], [])
    # instSet = [instructions.add, instructions.sub, instructions.outbox]
    instSet = ["add", "sub"]
    result = beam(st, instSet, [2, 5], 2, 2)
    # print result
    # for entry in result:
    #     print entry
    # print enumerateInsts(st, instSet, 2)
