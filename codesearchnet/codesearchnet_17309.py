def get_consistent_edges(graph: BELGraph) -> Iterable[Tuple[BaseEntity, BaseEntity]]:
    """Yield pairs of (source node, target node) for which all of their edges have the same type of relation.

    :return: An iterator over (source, target) node pairs corresponding to edges with many inconsistent relations
    """
    for u, v in graph.edges():
        if pair_is_consistent(graph, u, v):
            yield u, v