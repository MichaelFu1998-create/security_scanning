def pair_is_consistent(graph: BELGraph, u: BaseEntity, v: BaseEntity) -> Optional[str]:
    """Return if the edges between the given nodes are consistent, meaning they all have the same relation.

    :return: If the edges aren't consistent, return false, otherwise return the relation type
    """
    relations = {data[RELATION] for data in graph[u][v].values()}

    if 1 != len(relations):
        return

    return list(relations)[0]