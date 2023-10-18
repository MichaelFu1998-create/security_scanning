def get_contradictory_pairs(graph: BELGraph) -> Iterable[Tuple[BaseEntity, BaseEntity]]:
    """Iterates over contradictory node pairs in the graph based on their causal relationships
    
    :return: An iterator over (source, target) node pairs that have contradictory causal edges
    """
    for u, v in graph.edges():
        if pair_has_contradiction(graph, u, v):
            yield u, v