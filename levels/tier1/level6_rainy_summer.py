from state import State
from verifier import verify
import sympy

x, y = sympy.symbols('x y')

initial_state = State([x, y], [])
desired_output = State([x + y])


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
