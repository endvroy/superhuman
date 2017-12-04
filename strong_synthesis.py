import instructions
import itertools
import os
from collections import namedtuple
from collections import defaultdict

from state import State
from linetuple import LineTuple

from sympy import *

beamState = namedtuple("beamState", "lineInst, backptr, score, order")
backPtrs = {}
terminateStates = []

def computePrefix(candidate, target):
    if len(candidate) > len(target):
        return []
    else:
        for i in range(len(candidate)):
            if candidate[i] != target[i]:
                return []
        return candidate

def scoreInstruction(state, target):
    # Linear combination of 
    return 0.0

def evaluateRealInstOrder(currentInst, lastLine):
    newOrder = 0
    if currentInst.operator == "outbox" or currentInst.operator == "inbox":
        newOrder = 2
    else:
        newOrder = 3
    if lastLine != None:
        # print(lastLine)
        newOrder += lastLine.order
        if currentInst.copyFrom == lastLine.lineInst.copyTo:
            if currentInst.loc != lastLine.lineInst.copyTo:
                newOrder -= 2
            else:
                newOrder -= 1
    return newOrder

def enumerateInstruction(state, instructions, lastLine, target):
    lineInsts = []
    if state.mem is not None:
        validMemIndex = []
        for i in range(len(state.mem)):
            if state.mem[i] is not None:
                validMemIndex.append(i)
                lineInsts.append(LineTuple("outbox", state, copyFrom=i))
            if len(state.input) > 0:
                lineInsts.append(LineTuple("inbox", state, copyTo=i))
        rawLineInsts = list(itertools.product(instructions, validMemIndex, validMemIndex, range(len(state.mem))))
        for line in rawLineInsts:
            lineInsts.append(LineTuple(line[0], state, line[1], line[2], line[3]))
    stateTuples = []
    for inst in lineInsts:
        # Evaluate the order of the instruction
        # print('&& - ', lastLine)
        if lastLine is not None:
            # print ('&&& - ', lastLine)
            for (lastState, lastIndex) in lastLine:
                newOrder = evaluateRealInstOrder(inst, lastState)
                stateTuples.append(beamState(inst, None, scoreInstruction(inst, target), newOrder))
        else:
            newOrder = evaluateRealInstOrder(inst, lastLine)
            stateTuples.append(beamState(inst, None, scoreInstruction(inst, target), newOrder))
    # if len(lineInsts) > 0 and lastLine is not []:
    #     lastLine.lineInst.hasNext = True
    return stateTuples

def shouldPrune(state, target):
    output = state.output
    # commonPrefix = os.path.commonprefix([output, target])
    commonPrefix = computePrefix(output, target)
    if len(commonPrefix) < len(output) or len(output) > len(target):
        return True
    return False

def shouldTerminate(state, target):
    output = state.output
    # commonPrefix = os.path.commonprefix([output, target])
    commonPrefix = computePrefix(output, target)
    if len(commonPrefix) == len(output) and len(commonPrefix) == len(target):
        return True
    return False

def printStack(stack):
    for states in stack.keys():
        print (states)
    print('\n')

def extractInst(beamstate, stackIndex=-1):
    # return [] if beamstate is None else extractInst(beamstate.backptr) + [beamstate.lineInst]
    # print ("- ", beamstate)
    if beamstate is None:
        return []
    else:
        result = []
        # print ((beamstate.lineInst.state, stackIndex))
        backstates = backPtrs[(beamstate.lineInst.state, stackIndex)]
        if backstates == []:
            result.append([beamstate.lineInst])
        for (backState, backIndex) in backstates:
            lastInsts = extractInst(backState, backState.order) 
            for lastInst in lastInsts:
                # print('*', lastInst)
                result.append(lastInst + [beamstate.lineInst])
        return result

def beam(beginst, instSet, target, lineLimit, pruneLimit):
    # Key: current 
    lineLimit += 1
    stacks = [{} for _ in range(lineLimit)]

    enumInst = enumerateInstruction(beginst, instSet, None, target)
    for newstate in enumInst:
        if newstate.order < lineLimit:
            if not shouldPrune(newstate.lineInst.state, target):
                if newstate.lineInst.state not in stacks[newstate.order]:
                    stacks[newstate.order][newstate.lineInst.state] = []
                stacks[newstate.order][newstate.lineInst.state].append((newstate, 0))
                if (newstate.lineInst.state, newstate.order) not in backPtrs:
                    backPtrs[(newstate.lineInst.state, newstate.order)] = []

    for i in range(lineLimit - 1): 
        for statekey in stacks[i].keys():
            # print ('^^ - ', stacks[i][statekey])
            tempEqualList = {}
            enumInst = enumerateInstruction(statekey, instSet, stacks[i][statekey], target)
            for newstate in enumInst:
                # print ('new state order: ', newstate.order, ' stack: ', i)
                if not shouldTerminate(newstate.lineInst.state, target):
                    if newstate.order < lineLimit and newstate.order != i:
                        if not shouldPrune(newstate.lineInst.state, target):
                            if newstate.lineInst.state not in stacks[newstate.order]:
                                stacks[newstate.order][newstate.lineInst.state] = []
                            stacks[newstate.order][newstate.lineInst.state].append((newstate, i))
                            if (newstate.lineInst.state, newstate.order) not in backPtrs:
                                backPtrs[(newstate.lineInst.state, newstate.order)] = []
                            backPtrs[(newstate.lineInst.state, newstate.order)] += stacks[i][statekey]
                    # TODO: Deal with equal cases
                    elif newstate.order < lineLimit and newstate.order == i:
                        if not shouldPrune(newstate.lineInst.state, target):
                            if newstate.lineInst.state not in tempEqualList:
                                tempEqualList[newstate.lineInst.state] = []
                            tempEqualList[newstate.lineInst.state].append((newstate, i))
                            if (newstate.lineInst.state, newstate.order) not in backPtrs:
                                backPtrs[(newstate.lineInst.state, newstate.order)] = []
                            backPtrs[(newstate.lineInst.state, newstate.order)] += stacks[i][statekey]
                    else:
                        pass
                else:
                    terminateStates.append(newstate)
                    if (newstate.lineInst.state, newstate.order) not in backPtrs:
                        backPtrs[(newstate.lineInst.state, newstate.order)] = []
                    backPtrs[(newstate.lineInst.state, newstate.order)] += stacks[i][statekey]

            for statekey in tempEqualList.keys():
                enumInst = enumerateInstruction(statekey, instSet, tempEqualList[statekey], target)
                for newstate in enumInst:
                    # print ('new state order: ', newstate.order, ' stack: ', i)
                    if not shouldTerminate(newstate.lineInst.state, target):
                        if newstate.order < lineLimit:
                            if not shouldPrune(newstate.lineInst.state, target):
                                if newstate.lineInst.state not in stacks[newstate.order]:
                                    stacks[newstate.order][newstate.lineInst.state] = []
                                stacks[newstate.order][newstate.lineInst.state].append((newstate, i))
                                if (newstate.lineInst.state, newstate.order) not in backPtrs:
                                    backPtrs[(newstate.lineInst.state, newstate.order)] = []
                                backPtrs[(newstate.lineInst.state, newstate.order)] += tempEqualList[statekey]
                    else:
                        terminateStates.append(newstate)
                        if (newstate.lineInst.state, newstate.order) not in backPtrs:
                            backPtrs[(newstate.lineInst.state, newstate.order)] = []
                        backPtrs[(newstate.lineInst.state, newstate.order)] += stacks[i][statekey]

    for i, stack in enumerate(stacks):
        print("stack " + str(i) + " :")
        # printStack(stack)
    i = lineLimit - 1
    # while len(stacks[i]["outbox"]) == 0:
    #     i -= 1
    # insts = []
    # for state in stacks[i]["outbox"].values():
    #     insts.append(extractInst(state))
    # return insts
    # print('BackPtrs')
    # for statekey in backPtrs.keys():
    #     print (statekey, ': ', backPtrs[statekey])

    insts = []
    for state in terminateStates:
        print ("Extracting: ", state)
        insts += extractInst(state, state.order)
    print ('Insts:')
    for inst in insts:
        print (inst)

if __name__ == '__main__':
    x = symbols('x')
    tar = 8*x
    st = State([2], [None, None], [])
    # instSet = [instructions.add, instructions.sub, instructions.outbox]
    instSet = ["add", "sub"]
    result = beam(st, instSet, [80], 10, 2)
    print('test:')
    # for entry in result:
    #     print(entry)
        # print enumerateInsts(st, instSet, 2)
