def all_edges_consistent(graph):
    """Return if all edges are consistent in a graph. Wraps :func:`pybel_tools.utils.is_edge_consistent`.

    :param pybel.BELGraph graph: A BEL graph
    :return: Are all edges consistent
    :rtype: bool
    """
    return all(
        is_edge_consistent(graph, u, v)
        for u, v in graph.edges()
    )