def get_peripheral_successor_edges(graph: BELGraph, subgraph: BELGraph) -> EdgeIterator:
    """Get the set of possible successor edges peripheral to the sub-graph.

    The source nodes in this iterable are all inside the sub-graph, while the targets are outside.
    """
    for u in subgraph:
        for _, v, k in graph.out_edges(u, keys=True):
            if v not in subgraph:
                yield u, v, k