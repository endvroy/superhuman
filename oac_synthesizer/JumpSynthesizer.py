import sys
import instructions
from copy import deepcopy
from collections import namedtuple
from state import State, Cell
import pprint
pp = pprint.PrettyPrinter(indent=4)


BeamState = namedtuple('BeamState', 'st, inst, args, jump_locs, preds')

def stackSearchWithJump(initial_sts, instSet, jumpInstSet, depth, outputs):
    frontier = [BeamState(tuple(initial_sts), None, None, [], None)]

    for i in range(depth):
        sys.stderr.write("search depth : %d/%d, len = %d\n" % (i, depth, len(frontier)))
        new_frontier = []
        for j, b_st in enumerate(frontier):
            if j % 10000 == 0:
                sys.stderr.write("\tsearch: %d/%d\n" % (j, len(frontier)))
            state = b_st.st
            for newSt, inst, args in generate_insts(b_st, instSet):
                #print newSt, inst, args
                new_frontier.append(BeamState(newSt, inst, args, deepcopy(b_st.jump_locs), b_st))
            # synthesize jumps
            for newSt, inst, args, new_jump_locs in generate_jumps(b_st, jumpInstSet):
                #print newSt, inst, args
                new_frontier.append(BeamState(newSt, inst, args, new_jump_locs, b_st))
        frontier = new_frontier

    # filter out states with inconsistent inputs
    for b_st in frontier:
        #print map(lambda st: st.output, b_st.st)
        if map(lambda st: st.output, b_st.st) == outputs:
            _, all_insts = get_all_insts(b_st)
            yield map(lambda h: (h.inst, h.args), all_insts)

def DfsWithJump(initial_sts, instSet, jumpInstSet, depth, outputs):
    b_st = BeamState(tuple(initial_sts), None, None, [], None)
    return dfs(b_st, instSet, jumpInstSet, 0, depth, outputs)

def dfs(b_st, instSet, jumpInstSet, i, depth, outputs):
    if i == depth:
        # output insts with consistent output
        if map(lambda st: st.output, b_st.st) == outputs:
            _, all_insts = get_all_insts(b_st)
            yield map(lambda h: (h.inst, h.args), all_insts)
    else:
        for newSt, inst, args in generate_insts(b_st, instSet):
            #print newSt, inst, args
            new_b_st = BeamState(newSt, inst, args, deepcopy(b_st.jump_locs), b_st)
            for insts in dfs(new_b_st, instSet, jumpInstSet, i+1, depth, outputs):
                yield insts
        # synthesize jumps
        for newSt, inst, args, new_jump_locs in generate_jumps(b_st, jumpInstSet):
            #print newSt, inst, args
            new_b_st = BeamState(newSt, inst, args, new_jump_locs, b_st)
            for insts in dfs(new_b_st, instSet, jumpInstSet, i+1, depth, outputs):
                yield insts

# inst generators
def generate_add(b_st):
    states = b_st.st
    # check if all reg is non empty
    mem_len = len(states[0].mem)
    if not any(map(lambda st: st.reg.is_empty(), states)):
        for loc in range(mem_len):
            if not any(map(lambda st: st.mem[loc].is_empty(), states)):
                yield (map(lambda st: instructions.add(st, loc), states), [loc])

def generate_sub(b_st):
    states = b_st.st
    mem_len = len(states[0].mem)
    if not any(map(lambda st: st.reg.is_empty(), states)):
        for loc in range(mem_len):
            if not any(map(lambda st: st.mem[loc].is_empty(), states)):
                yield (map(lambda st: instructions.sub(st, loc), states), [loc])

def generate_inbox(b_st):
    states = b_st.st
    if all(map(lambda st:st.input, states)):
        yield (map(lambda st: instructions.inbox(st), states), [])

def generate_outbox(b_st):
    states = b_st.st
    if not any(map(lambda st: st.reg.is_empty(), states)):
        yield (map(lambda st: instructions.outbox(st), states), [])

def generate_copyTo(b_st):
    states = b_st.st
    mem_len = len(states[0].mem)
    if not any(map(lambda st: st.reg.is_empty(), states)):
        empty_slot_used = False
        for loc in range(mem_len):
            if all(map(lambda st:st.mem[loc].is_empty(), states)):
                if empty_slot_used:
                    break
                else:
                    empty_slot_used = True
            # maybe do something with used bit here
            yield (map(lambda st: instructions.copyTo(st, loc), states), [loc])

def generate_copyFrom(b_st):
    states = b_st.st
    mem_len = len(states[0].mem)
    for loc in range(mem_len):
        if not any(map(lambda st:st.mem[loc].is_empty(), states)):
            yield (map(lambda st:instructions.copyFrom(st, loc), states), [loc])

def generate_insts(b_st, instSet):
    for inst in instSet:
        generator = inst_generator_map[inst]
        for newSt, args in generator(b_st):
            yield (newSt, inst, args)

#----------------------------------------------------
# generate all possible jumps

h_tuple = namedtuple('History', 'inst, args, st')
jumpFromFuncs = {
    instructions.jump : instructions.jumpFrom,
    instructions.jumpIfZero : instructions.jumpIfZeroFrom,
    instructions.jumpIfNegative : instructions.jumpIfNegativeFrom}
jumpFuncs = {
    instructions.jumpFrom : instructions.jump,
    instructions.jumpIfZeroFrom : instructions.jumpIfZero,
    instructions.jumpIfNegativeFrom : instructions.jumpIfNegative
}
jumpConditions = {
    instructions.jump : lambda st: True,
    instructions.jumpIfZero : lambda st: st.reg.val == 0,
    instructions.jumpIfNegative : lambda st: st.reg.val < 0
}

def generate_jumps(b_st, jumpInstSet):
    initial_st, prev_insts = get_all_insts(b_st)
    for jumpInst in jumpInstSet:
        generator = inst_generator_map[jumpInst]
        for newSt, args, new_jump_locs in generator(b_st, jumpInst, initial_st, prev_insts):
            yield (newSt, jumpFromFuncs[jumpInst], args, new_jump_locs)

def jump_generator(b_st, jump_type, initial_st, prev_insts):
    # get jump jump condition
    jump_cond = jumpConditions[jump_type]

    # initialize res
    generatedJumps = []
    for i in range(len(prev_insts)+1):
        generatedJumps.append([(), [], getNewJumpLocs(b_st, i)])

    # jump from other positions
    for k in range(len(initial_st)):
        current_st = initial_st[k]
        last_st = b_st.st[k]
        nextJumpPos = -1
        for i in range(len(prev_insts)):
            # decide jumped state
            if i <= nextJumpPos:
                generatedJumps[i][0] += (last_st,)
                continue
            elif not current_st.reg.is_empty() or jump_type == instructions.jump:
                # if jump cond is satisfied, jump
                jumpedSt = current_st if jump_cond(current_st) else last_st
                generatedJumps[i][0] += (jumpedSt,)

            # update current st
            # if current inst is a jump, jump if possible
            current_inst = prev_insts[i].inst
            if current_inst in jumpFuncs.values():
                # current is not changed
                # update nextJumpPos if jump condition is True
                if jumpConditions[current_inst](current_st):
                    nextJumpPos = prev_insts[i].args[0]
            else:
                current_st = prev_insts[i].st[k]

        generatedJumps[-1][0] = b_st.st

    # output result
    for j in generatedJumps:
        # yield something
        pass

    res = map(tuple, filter(lambda j: len(j[0]) == len(initial_st), generatedJumps))
    return res

def getNewJumpLocs(b_st, loc):
    return map(lambda x: x if x < loc else x+1, b_st.jump_locs) + [loc]




def extract_history(b_st):
    return extract_history(b_st.preds)+[h_tuple(b_st.inst, deepcopy(b_st.args), b_st.st)] if b_st.preds else [b_st.st]

def get_all_insts(b_st):
    history = extract_history(b_st)
    initial_st = history[0]
    history = history[1:]

    # get all jumpFroms in history=
    # put jump loc into history
    i, j = 0, 0
    all_jumps = []
    while i < len(history):
        if history[i].inst in jumpFromFuncs.values():
            all_jumps.append(history[i])
            history[i].args.append(b_st.jump_locs[j])
            j += 1
        i += 1

    # number jumps should equal jump_locs
    assert len(all_jumps) == len(b_st.jump_locs)

    # insert jumps into instructions
    all_jumps.sort(key=lambda h: h.args)
    for jump in all_jumps:
        history.insert(jump.args[0], h_tuple(jumpFuncs[jump.inst], [], None))

    # add jump locs
    for i, h in enumerate(history):
        if h.inst in jumpFromFuncs.values():
            history[h.args[0]].args.append(i)

    return (initial_st, history)

inst_generator_map = {
    instructions.add : generate_add,
    instructions.sub : generate_sub,
    instructions.copyTo : generate_copyTo,
    instructions.copyFrom : generate_copyFrom,
    instructions.inbox : generate_inbox,
    instructions.outbox : generate_outbox,
    instructions.jump : jump_generator,
    instructions.jumpIfZero : jump_generator,
    instructions.jumpIfNegative: jump_generator
}
