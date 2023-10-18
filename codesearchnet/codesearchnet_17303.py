def count_unique_relations(graph: BELGraph) -> Counter:
    """Return a histogram of the different types of relations present in a graph.

    Note: this operation only counts each type of edge once for each pair of nodes
    """
    return Counter(itt.chain.from_iterable(get_edge_relations(graph).values()))