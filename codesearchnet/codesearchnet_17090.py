def remove_highlight_edges(graph: BELGraph, edges=None):
    """Remove the highlight from the given edges, or all edges if none given.

    :param graph: A BEL graph
    :param edges: The edges (4-tuple of u,v,k,d) to remove the highlight from)
    :type edges: iter[tuple]
    """
    for u, v, k, _ in graph.edges(keys=True, data=True) if edges is None else edges:
        if is_edge_highlighted(graph, u, v, k):
            del graph[u][v][k][EDGE_HIGHLIGHT]