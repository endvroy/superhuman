from functools import partial


def verify(instrs, initial_state, criteria):
    """apply the instructions to the start state
     and check if the result state can pass the criteria
     criteria should be a function with the following signature:
     criteria(end_state) -> True if passed, False otherwise"""
    state = initial_state
    for instr in instrs:
        state = instr(state)  # convert to partial functions with the adapter

    return criteria(state)


# todo: test the adapter
def instrs_adapter(linetuples):
    return (partial(x.operator,
                    copyFrom=x.copyFrom,
                    loc=x.loc,
                    copyTo=x.copyTo)
            for x in linetuples)


if __name__ == '__main__':
    from linetuple import LineTuple
    from instructions import add, sub, outbox
    from state import State

    init_state = State([7, 42, 1337], [44])
    linetuples = [LineTuple(add, 'spam', 1, 2, 3),
                  LineTuple(outbox, 'spam', 2),
                  LineTuple(sub, 'spam', 3, 1, 1)]


    def criteria(final_state: State):
        return final_state.mem == [42 + 1337, 42, 7 + 42 + 1337] \
               and final_state.output == [42]


    print(verify(instrs_adapter(linetuples), init_state, criteria))
