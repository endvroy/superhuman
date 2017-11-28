from state import State
from verifier import verify
import sympy

x = sympy.symbols('x')

initial_state = State([x], [])
desired_output = [40 * x]


def criteria(end_state: State):
    if end_state.output == desired_output:
        return True
    else:
        return False


# todo: fill in
candidates = []  # get all possible instructions
for instrs in candidates:
    if verify(instrs, initial_state, criteria):
        pass  # passed
