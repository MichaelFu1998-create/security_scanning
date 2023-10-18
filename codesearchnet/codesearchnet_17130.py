def get_peripheral_predecessor_edges(graph: BELGraph, subgraph: BELGraph) -> EdgeIterator:
    """Get the set of possible predecessor edges peripheral to the sub-graph.

    The target nodes in this iterable are all inside the sub-graph, while the sources are outside.
    """
    for v in subgraph:
        for u, _, k in graph.in_edges(v, keys=True):
            if u not in subgraph:
                yield u, v, k