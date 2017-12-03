import sympy
from oac_synthesizer.state import State
from oac_synthesizer.verifiedSynthesizer import verifiedSearch
import oac_synthesizer.instructions as instructions
from pprint import pprint

x = sympy.symbols('x')

initial_state = State((x,), None, [None, None, None], ())
desired_output = 3 * x,


def criteria(end_state: State):
    if end_state.output == desired_output:
        return True
    else:
        return False


candidates = verifiedSearch(initial_state,
                            [instructions.add,
                             instructions.copyFrom,
                             instructions.copyTo,
                             instructions.inbox,
                             instructions.outbox],
                            5,
                            desired_output)
pprint(list(candidates))
