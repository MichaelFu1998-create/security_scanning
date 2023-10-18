def infer_missing_backwards_edge(graph, u, v, k):
    """Add the same edge, but in the opposite direction if not already present.

    :type graph: pybel.BELGraph
    :type u: tuple
    :type v: tuple
    :type k: int
    """
    if u in graph[v]:
        for attr_dict in graph[v][u].values():
            if attr_dict == graph[u][v][k]:
                return

    graph.add_edge(v, u, key=k, **graph[u][v][k])