def get_correlation_triangles(graph: BELGraph) -> SetOfNodeTriples:
    """Return a set of all triangles pointed by the given node."""
    return {
        tuple(sorted([n, u, v], key=str))
        for n in graph
        for u, v in itt.combinations(graph[n], 2)
        if graph.has_edge(u, v)
    }