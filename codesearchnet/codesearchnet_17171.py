def pair_has_contradiction(graph: BELGraph, u: BaseEntity, v: BaseEntity) -> bool:
    """Check if a pair of nodes has any contradictions in their causal relationships.

    Assumes both nodes are in the graph.
    """
    relations = {data[RELATION] for data in graph[u][v].values()}
    return relation_set_has_contradictions(relations)