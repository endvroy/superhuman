import sys
import instructions
from collections import namedtuple
from state import State, Cell

BeamState = namedtuple('BeamState', 'st, inst, args, preds')


def stackSearch(initial_st, instSet, depth, output):
    stacks = [{} for _ in range(depth + 1)]
    stacks[0][initial_st] = [BeamState(initial_st, None, None, None)]

    for i, stack in enumerate(stacks[:-1]):
        sys.stderr.write("search depth : %d/%d, len = %d\n" % (i, depth, len(stack)))
        for state in stack.keys():
            for newSt, inst, args in generate_insts(state, instSet, output):
                newBeamSt = BeamState(newSt, inst, args, stack[state])
                if newSt in stacks[i+1]:
                    stacks[i+1][newSt].append(newBeamSt)
                else:
                    stacks[i+1][newSt] = [newBeamSt]

    for st, final_states in stacks[-1].items():
        if st.output != output:
            continue
        for final_st in final_states:
            for candidate in extractInsts(final_st):
                yield candidate


def extractInsts(b_st):
    if not b_st.preds:
        yield []
    else:
        for pred in b_st.preds:
            for insts in extractInsts(pred):
                yield insts + [(b_st.inst, b_st.args)]

# inst generators
def generate_add(st, output):
    if not st.reg.is_empty():
        for loc in range(len(st.mem)):
            if not st.mem[loc].is_empty():
                yield (instructions.add(st, loc), [loc])


def generate_sub(st, output):
    if not st.reg.is_empty():
        for loc in range(len(st.mem)):
            if not st.mem[loc].is_empty():
                yield (instructions.sub(st, loc), [loc])


def generate_inbox(st, output):
    if st.input:
        yield (instructions.inbox(st), [])


def generate_outbox(st, output):
    if not st.reg.is_empty() and len(st.output) < len(output):
        if st.reg.val == output[len(st.output)]:
            yield (instructions.outbox(st), [])


def generate_copyTo(st, output):
    if not st.reg.is_empty():
        empty_slot_used = False
        for loc in range(len(st.mem)):
            if st.mem[loc].is_empty():
                # only copy to first empty slot
                if empty_slot_used:
                    break
                empty_slot_used = True
            elif not st.mem[loc].used:
                # only copy to used loc
                continue
            yield (instructions.copyTo(st, loc), [loc])


def generate_copyFrom(st, output):
    if st.reg.is_empty() or st.reg.used:
        for loc in range(len(st.mem)):
            if not st.mem[loc].is_empty():
                yield (instructions.copyFrom(st, loc), [loc])


inst_generator_map = {
    instructions.add: generate_add,
    instructions.sub: generate_sub,
    instructions.copyTo: generate_copyTo,
    instructions.copyFrom: generate_copyFrom,
    instructions.inbox: generate_inbox,
    instructions.outbox: generate_outbox
}


def generate_insts(st, instSet, output):
    for inst in instSet:
        generator = inst_generator_map[inst]
        for newSt, args in generator(st, output):
            yield (newSt, inst, args)
