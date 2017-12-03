import sympy
from oac_synthesizer.state import State
from oac_synthesizer.synthesizer import stackSearch
import oac_synthesizer.instructions as instructions
from oac_synthesizer.verify.verifier import verify
from pprint import pprint

x = sympy.symbols('x')

initial_state = State((x,), None, [None, None, None], ())
desired_output = 8 * x,


def criteria(end_state: State):
    if end_state.output == desired_output:
        return True
    else:
        return False


candidates = stackSearch(initial_state,
                         [instructions.add,
                          instructions.copyFrom,
                          instructions.copyTo,
                          instructions.inbox,
                          instructions.outbox],
                         8,
                         desired_output)
passed = []
for instrs in candidates:
    if verify(instrs, initial_state, criteria):
        passed.append(instrs)
pprint(passed)
