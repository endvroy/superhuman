from state import State
from verifier import verify

mem = [x.encode('ascii') for x in 'UJXGBE']
initial_state = State(mem, [])

desired_output = [x.encode('ascii') for x in 'BUG']


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
