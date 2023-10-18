def get_contradiction_summary(graph: BELGraph) -> Iterable[Tuple[BaseEntity, BaseEntity, str]]:
    """Yield triplets of (source node, target node, set of relations) for (source node, target node) pairs
    that have multiple, contradictory relations.
    """
    for u, v in set(graph.edges()):
        relations = {data[RELATION] for data in graph[u][v].values()}
        if relation_set_has_contradictions(relations):
            yield u, v, relations