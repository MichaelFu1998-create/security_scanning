def get_triangles(graph: DiGraph) -> SetOfNodeTriples:
    """Get a set of triples representing the 3-cycles from a directional graph.

    Each 3-cycle is returned once, with nodes in sorted order.
    """
    return {
        tuple(sorted([a, b, c], key=str))
        for a, b in graph.edges()
        for c in graph.successors(b)
        if graph.has_edge(c, a)
    }