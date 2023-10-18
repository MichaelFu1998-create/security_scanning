def highlight_edges(graph: BELGraph, edges=None, color: Optional[str]=None) -> None:
    """Adds a highlight tag to the given edges.

    :param graph: A BEL graph
    :param edges: The edges (4-tuples of u, v, k, d) to add a highlight tag on
    :type edges: iter[tuple]
    :param str color: The color to highlight (use something that works with CSS)
    """
    color = color or EDGE_HIGHLIGHT_DEFAULT_COLOR
    for u, v, k, d in edges if edges is not None else graph.edges(keys=True, data=True):
        graph[u][v][k][EDGE_HIGHLIGHT] = color