def is_edge_highlighted(graph: BELGraph, u, v, k) -> bool:
    """Returns if the given edge is highlighted.
    
    :param graph: A BEL graph
    :return: Does the edge contain highlight information?
    :rtype: bool
    """
    return EDGE_HIGHLIGHT in graph[u][v][k]