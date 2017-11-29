from functools import partial


def verify(linetuples, initial_state, criteria):
    """apply the instructions to the start state
     and check if the result state can pass the criteria
     criteria should be a function with the following signature:
     criteria(end_state) -> True if passed, False otherwise"""
    state = initial_state
    for linetuple in linetuples:
        opcode, args = linetuple.getInstWithArgs()
        state = opcode(state, *args)  # convert to partial functions with the adapter

    return criteria(state)


if __name__ == '__main__':
    from linetuple import LineTuple
    from state import State

    init_state = State([7, 42, 1337], [44])
    linetuples = [LineTuple('add', init_state, 0, 1, 1),
                  LineTuple('outbox', init_state, 1),
                  LineTuple('sub', init_state, 2, 0, 0)]


    # print(init_state)


    def criteria(final_state: State):
        # print(final_state)
        return final_state.mem == [1330, 49, 1337] \
               and final_state.output == [44, 49]


    print(verify(linetuples, init_state, criteria))
