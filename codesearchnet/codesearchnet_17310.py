def infer_missing_two_way_edges(graph):
    """Add edges to the graph when a two way edge exists, and the opposite direction doesn't exist.

    Use: two way edges from BEL definition and/or axiomatic inverses of membership relations

    :param pybel.BELGraph graph: A BEL graph
    """
    for u, v, k, d in graph.edges(data=True, keys=True):
        if d[RELATION] in TWO_WAY_RELATIONS:
            infer_missing_backwards_edge(graph, u, v, k)