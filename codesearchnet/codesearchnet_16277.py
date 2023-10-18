def get_levels(G):
    """
    For the parallel topo sort to work, the targets have
    to be executed in layers such that there is no
    dependency relationship between any nodes in a layer.
    What is returned is a list of lists representing all
    the layers, or levels
    """
    levels = []
    ends = get_sinks(G)
    levels.append(ends)
    while get_direct_ancestors(G, ends):
        ends = get_direct_ancestors(G, ends)
        levels.append(ends)
    levels.reverse()
    return levels