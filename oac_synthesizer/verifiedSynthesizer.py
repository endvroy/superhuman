from oac_synthesizer.synthesizer import generate_insts
from collections import namedtuple

SearchNode = namedtuple('SearchNode', 'st, inst, args, pred, depth')


def verifiedSearch(initial_st, instSet, depth, output):
    frontier = [SearchNode(initial_st, None, None, None, 0)]
    seen = {initial_st}

    while frontier:
        node = frontier.pop()
        for newSt, inst, args in generate_insts(node.st, instSet, output):
            new_node = SearchNode(newSt, inst, args, node, node.depth + 1)
            if new_node.depth == depth:
                if new_node.st.output == output:
                    return extract_seq(new_node)
                else:
                    continue
            if new_node.st not in seen:
                frontier.append(new_node)
                seen.add(new_node.st)


def extract_seq(search_node: SearchNode):
    seq = [(search_node.inst, search_node.args)]
    node = search_node.pred
    while node is not None:
        seq.append((node.inst, node.args))
        node = node.pred
    return reversed(seq[:-1])
