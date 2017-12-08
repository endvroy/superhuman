from state import State
import instructions
from synthesizer import stackSearch
from JumpSynthesizer import stackSearchWithJump, DfsWithJump
from JumpSynthesizer import get_all_insts, BeamState, jump_generator
import pprint
pp = pprint.PrettyPrinter(indent=4)


# zero room
'''
sts = [State((2,), None, [None], ()), State((0,), None, [None], ())]
instSet = [instructions.inbox, instructions.outbox]#, instructions.add, instructions.sub, instructions.copyTo, instructions.copyFrom]
jumpInstSet = [instructions.jumpIfZero, instructions.jump]

for insts in stackSearchWithJump(sts, instSet, jumpInstSet, 4, [(), (0,)]):
    #print map(lambda (i, args) : (i.__name__, args), insts)
    pp.pprint(insts)
'''

'''
# equalization room
sts = [State((), 2, [2], ()), State((), 2, [20], ())]
instSet = [instructions.inbox, instructions.outbox, instructions.sub, instructions.copyTo, instructions.copyFrom]
jumpInstSet = [instructions.jumpIfZero, instructions.jump]

for insts in DfsWithJump(sts, instSet, jumpInstSet, 5, [(2,), ()]):
    #print map(lambda (i, args) : (i.__name__, args), insts)
    pp.pprint(insts)
'''


sts = [State((), 5, [2, None], ()), State((), 11, [20, None], ())]
instSet = [instructions.inbox, instructions.outbox, instructions.sub, instructions.add, instructions.copyTo, instructions.copyFrom]
jumpInstSet = [instructions.jumpIfNegative, instructions.jump]

for insts in DfsWithJump(sts, instSet, jumpInstSet, 6, [(5,), (20,)]):
    pp.pprint(map(lambda (i, args) : (i.__name__, args), insts))




'''
# synthesizer demo
st = State((3,), None, [None], ())
instSet = [instructions.inbox, instructions.outbox, instructions.add, instructions.sub, instructions.copyTo, instructions.copyFrom]

for insts in stackSearch(st, instSet, 13, (120,)):
    print map(lambda (i, args) : (i.__name__, args), insts)
    st = State((3,), None, [None], ())

    # run insts
    for inst, args in insts:
        print st
        st = inst(*([st]+args))
    print st
    print
'''







# instructions demo
'''
st = State((1,), None, [2, None, 4], ())
print st
st = instructions.inbox(st)
print st
st = instructions.outbox(st)
print st
st = instructions.add(st, 0)
print st
st = instructions.copyFrom(st, 0)
print st
st = instructions.copyTo(st, 0)
print st
st = instructions.sub(st, 0)
print st
st = instructions.outbox(st)
print st
'''
