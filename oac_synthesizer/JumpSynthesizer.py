import sys
import instructions
from collections import namedtuple
from state import State, Cell

BeamState = namedtuple('BeamState', 'st, inst, args, preds')

def stackSearchWithJump(initial_sts, instSet, depth, outputs):
    frontier = [BeamState(tuple(initial_sts), None, None, None)]

    for i in range(depth):
        #sys.stderr.write("search depth : %d/%d, len = %d\n" % (i, depth, len(frontier)))
        new_frontier = []
        for b_st in frontier:
            state = b_st.st
            for newSt, inst, args in generate_insts(state, instSet):
                new_frontier.append(BeamState(newSt, inst, args, b_st))
        frontier = new_frontier

    # filter out states with inconsistent inputs
    for b_st in frontier:
        if map(lambda st: st.output, b_st.st) == outputs:
            yield extract(b_st)

def extract(st):
    return extract(st.preds)+[(st.inst, st.args)] if st.preds else []


# inst generators
def generate_add(states):
    # check if all reg is non empty
    mem_len = len(states[0].mem)
    if not any(map(lambda st: st.reg.is_empty(), states)):
        for loc in range(mem_len):
            if not any(map(lambda st: st.mem[loc].is_empty(), states)):
                yield (map(lambda st: instructions.add(st, loc), states), [loc])

def generate_sub(states):
    mem_len = len(states[0].mem)
    if not any(map(lambda st: st.reg.is_empty(), states)):
        for loc in range(mem_len):
            if not any(map(lambda st: st.mem[loc].is_empty(), states)):
                yield (map(lambda st: instructions.sub(st, loc), states), [loc])

def generate_inbox(states):
    if all(map(lambda st:st.input, states)):
        yield (map(lambda st: instructions.inbox(st), states), [])

def generate_outbox(states):
    if not any(map(lambda st: st.reg.is_empty(), states)):
        yield (map(lambda st: instructions.outbox(st), states), [])

def generate_copyTo(states):
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

def generate_copyFrom(states):
    mem_len = len(states[0].mem)
    for loc in range(mem_len):
        if not any(map(lambda st:st.mem[loc].is_empty(), states)):
            yield (map(lambda st:instructions.copyFrom(st, loc), states), [loc])


def generate_insts(st, instSet):
    for inst in instSet:
        generator = inst_generator_map[inst]
        for newSt, args in generator(st):
            yield (newSt, inst, args)

inst_generator_map = {
    instructions.add : generate_add,
    instructions.sub : generate_sub,
    instructions.copyTo : generate_copyTo,
    instructions.copyFrom : generate_copyFrom,
    instructions.inbox : generate_inbox,
    instructions.outbox : generate_outbox
}
