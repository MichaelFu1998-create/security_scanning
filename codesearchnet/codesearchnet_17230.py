def rewire_targets(graph, rewiring_probability):
    """Rewire a graph's edges' target nodes.

    - For BEL graphs, assumes edge consistency (all edges between two given nodes are have the same relation)
    - Doesn't make self-edges

    :param pybel.BELGraph graph: A BEL graph
    :param float rewiring_probability: The probability of rewiring (between 0 and 1)
    :return: A rewired BEL graph
    """
    if not all_edges_consistent(graph):
        raise ValueError('{} is not consistent'.format(graph))

    result = graph.copy()
    nodes = result.nodes()

    for u, v in result.edges():
        if random.random() < rewiring_probability:
            continue

        w = random.choice(nodes)

        while w == u or result.has_edge(u, w):
            w = random.choice(nodes)

        result.add_edge(w, v)
        result.remove_edge(u, v)

    return result