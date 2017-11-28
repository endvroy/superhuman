def verify(instrs, initial_state, criteria):
    """apply the instructions to the start state
     and check if the result state can pass the criteria
     criteria should be a function with the following signature:
     criteria(end_state) -> True if passed, False otherwise"""
    state = initial_state
    for instr in instrs:
        state = instr(state)  # convert to partial functions with the adapter

    return criteria(state)

# todo: add an adapter
