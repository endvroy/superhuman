import instructions
from collections import namedtuple
from state import State
from state import Cell

BeamState = namedtuple('BeamState', 'st, inst, args, preds')

def stackSearch(initial_st, instSet, depth, output):
    stacks = [{} for _ in range(depth+1)]
    stacks[0][initial_st] = [BeamState(initial_st, None, None, None)]

    for i, stack in enumerate(stacks[:-1]):
         for state in stack.keys():
             for newSt, inst, args in generate_insts(state, instSet, output):
                 #print newSt, inst, args
                 newBeamSt = BeamState(newSt, inst, args, stack[state])
                 if newSt in stacks[i+1]:
                     stacks[i+1][newSt].append(newBeamSt)
                 else:
                     stacks[i+1][newSt] = [newBeamSt]

    candidates = []
    for st, final_states in stacks[-1].items():
        if st.output != output:
            continue
        print st.output, output
        for final_st in final_states:
            #print final_st.st
            candidates += extractInsts(final_st)
    return candidates

def extractInsts(b_st):
    if not b_st.inst:
        return [[]]

    res = []
    for pred in b_st.preds:
        res += [ insts + [(b_st.inst, b_st.args)] for insts in extractInsts(pred) ]
    return res


# inst generators
def generate_add(st, output):
    if st.reg.val:
        for loc in range(len(st.mem)):
            if st.mem[loc].val:
                yield (instructions.add(st, loc), [loc])

def generate_sub(st, output):
    if st.reg.val:
        for loc in range(len(st.mem)):
            if st.mem[loc].val:
                yield (instructions.sub(st, loc), [loc])

def generate_inbox(st, output):
    if st.input:
        yield (instructions.inbox(st), [])

def generate_outbox(st, output):
    if st.reg.val and len(st.output) < len(output):
        if st.reg.val == output[len(st.output)]:
            yield (instructions.outbox(st), [])

def generate_copyTo(st, output):
    if st.reg.val:
        for loc in range(len(st.mem)):
            # only copy to used loc
            if not st.mem[loc].val or st.mem[loc].used:
                yield (instructions.copyTo(st, loc), [loc])

def generate_copyFrom(st, output):
    if not st.reg.val or st.reg.used:
        for loc in range(len(st.mem)):
            if st.mem[loc].val:
                yield (instructions.copyFrom(st, loc), [loc])

inst_generator_map = {
    instructions.add : generate_add,
    instructions.sub : generate_sub,
    instructions.copyTo : generate_copyTo,
    instructions.copyFrom : generate_copyFrom,
    instructions.inbox : generate_inbox,
    instructions.outbox : generate_outbox
}

def generate_insts(st, instSet, output):
    for inst in instSet:
        generator = inst_generator_map[inst]
        for newSt, args in generator(st, output):
            yield (newSt, inst, args)


if __name__ == '__main__':
    st = State((23,32), None, Cell.cell_array([None]), ())
    instSet = [instructions.inbox, instructions.outbox, instructions.add, instructions.sub, instructions.copyTo, instructions.copyFrom]

    for insts in stackSearch(st, instSet, 5, (55,)):
        print map(lambda (i, args) : (i.__name__, args), insts)
        st = State((23,32), None, Cell.cell_array([None]), ())
        for inst, args in insts:
            print st
            st = inst(*([st]+args))
        print st
