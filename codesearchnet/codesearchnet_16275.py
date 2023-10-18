def get_direct_ancestors(G, list_of_nodes):
    """
    Returns a list of nodes that are the parents
    from all of the nodes given as an argument.
    This is for use in the parallel topo sort
    """
    parents = []
    for item in list_of_nodes:
        anc = G.predecessors(item)
        for one in anc:
            parents.append(one)
    return parents