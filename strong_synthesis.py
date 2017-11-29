import instructions
import itertools
import os
from collections import namedtuple
from collections import defaultdict

from state import State
from linetuple import LineTuple

beamState = namedtuple("beamState", "lineInst, backptr, score, order")


def scoreInstruction(state, target):
    # Linear combination of 
    return 0.0


def evaluateRealInstOrder(currentInst, lastLine):
    newOrder = 0
    if currentInst.operator == "outbox":
        newOrder = 2
    else:
        newOrder = 3
    if lastLine is not None:
        newOrder += lastLine.order
        if currentInst.copyFrom == lastLine.lineInst.copyTo and currentInst.loc != lastLine.lineInst.copyTo:
            if currentInst.operator == "outbox":
                newOrder -= 1
            else:
                newOrder -= 2
    return newOrder


def enumerateInstruction(state, instructions, lastLine, target):
    lineInsts = []
    if state.mem is not None:
        validMemIndex = []
        for i in range(len(state.mem)):
            if state.mem[i] is not None:
                validMemIndex.append(i)
                lineInsts.append(LineTuple("outbox", state, copyFrom=i))
        rawLineInsts = list(itertools.product(instructions, validMemIndex, validMemIndex, range(len(state.mem))))
        for line in rawLineInsts:
            lineInsts.append(LineTuple(line[0], state, line[1], line[2], line[3]))
    stateTuples = {"outbox": [], "arith": []}

    for inst in lineInsts:
        # Evaluate the order of the instruction
        newOrder = evaluateRealInstOrder(inst, lastLine)
        if inst.operator == "outbox":
            stateTuples["outbox"].append(beamState(inst, lastLine, scoreInstruction(inst, target), newOrder))
        else:
            stateTuples["arith"].append(beamState(inst, lastLine, scoreInstruction(inst, target), newOrder))
    if len(lineInsts) > 0 and lastLine is not None:
        lastLine.lineInst.hasNext = True
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
    for state in stack["outbox"].values():
        print('-', state)
    for state in stack["arith"].values():
        print('-', state)
    print('\n')


def extractInst(beamstate):
    return [] if beamstate is None else extractInst(beamstate.backptr) + [beamstate.lineInst]


def beam(beginst, instSet, target, lineLimit, pruneLimit):
    # Key: current 
    stacks = [{"outbox": {}, "arith": {}} for _ in range(lineLimit)]

    enumInst = enumerateInstruction(beginst, instSet, None, target)
    pruneStack(enumInst, target)
    # printStack(stacks[0])

    # stacks[0]["outbox"] = enumInst["outbox"]
    # stacks[0]["arith"] = enumInst["arith"]
    for state in enumInst["outbox"]:
        if state.order < lineLimit:
            if repr((state.lineInst.state.mem, state.lineInst.state.output)) not in stacks[state.order]["outbox"]:
                stacks[state.order]["outbox"][repr((state.lineInst.state.mem, state.lineInst.state.output))] = state
    for state in enumInst["arith"]:
        if state.order < lineLimit:
            if repr((state.lineInst.state.mem, state.lineInst.state.output)) not in stacks[state.order]["arith"]:
                stacks[state.order]["arith"][repr((state.lineInst.state.mem, state.lineInst.state.output))] = state

    for i in range(lineLimit - 1):
        for state in itertools.chain(stacks[i]["outbox"].values(), list(stacks[i]["arith"].values())):
            enumInst = enumerateNextInstruction(state, instSet, target)
            pruneStack(enumInst, target)
            for newstate in enumInst["outbox"]:
                if newstate.order < lineLimit:
                    if repr((newstate.lineInst.state.mem, newstate.lineInst.state.output)) not in \
                            stacks[newstate.order]["outbox"]:
                        stacks[newstate.order]["outbox"][
                            repr((newstate.lineInst.state.mem, newstate.lineInst.state.output))] = newstate
            for newstate in enumInst["arith"]:
                if newstate.order < lineLimit:
                    if repr((newstate.lineInst.state.mem, newstate.lineInst.state.output)) not in \
                            stacks[newstate.order]["arith"]:
                        stacks[newstate.order]["arith"][
                            repr((newstate.lineInst.state.mem, newstate.lineInst.state.output))] = newstate
                        # Evaluate
                        # printStack(stacks[i+1])
    for i, stack in enumerate(stacks):
        print("stack " + str(i) + " :")
        printStack(stack)
    i = lineLimit - 1
    while len(stacks[i]["outbox"]) == 0:
        i -= 1
    insts = []
    for state in stacks[i]["outbox"].values():
        insts.append(extractInst(state))
    return insts


if __name__ == '__main__':
    st = State([2, None, 3], [])
    # instSet = [instructions.add, instructions.sub, instructions.outbox]
    instSet = ["add", "sub"]
    result = beam(st, instSet, [2, 5, 3], 7, 2)
    print('test:')
    for entry in result:
        print(entry)
        # print enumerateInsts(st, instSet, 2)
