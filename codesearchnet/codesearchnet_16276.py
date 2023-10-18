def get_sinks(G):
    """
    A sink is a node with no children.
    This means that this is the end of the line,
    and it should be run last in topo sort. This
    returns a list of all sinks in a graph
    """
    sinks = []
    for node in G:
        if not len(list(G.successors(node))):
            sinks.append(node)
    return sinks