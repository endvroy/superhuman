import instructions
from state import State

def enumerateInsts(st, instSet, k):
    if k == 0:
        return [[]]

    insts_k = []
    for inst in instSet:
        argType = instructions.instArgsMap[inst]
        params = [[st]]
        # check register status is useReg is True
        if argType.useReg and st.reg is None:
            continue
        for t in argType.argList:
            if t == 'l': # memory access
                # check all memory locations
                validLocs = []
                for i in range(len(st.mem)):
                    if st.mem[i] is None:
                        # bypass invalid mem read
                        continue
                    validLocs.append(i)
                params = [ a + [b] for a in params for b in validLocs]
        for p in params:
            insts_k.append((inst, p))

    res = []
    for (inst, params) in insts_k:
        a = enumerateInsts(inst(*params), instSet, k-1);
        res += [ [(inst, params)] + tail for tail in a ]
    return res

if __name__ == '__main__':
    st = State(1, [2, None, 3], [])
    instSet = [instructions.add, instructions.sub, instructions.copyTo, instructions.copyFrom, instructions.outbox]
    print enumerateInsts(st, instSet, 5)
