def group_nodes_by_annotation(graph: BELGraph, annotation: str = 'Subgraph') -> Mapping[str, Set[BaseEntity]]:
    """Group the nodes occurring in edges by the given annotation."""
    result = defaultdict(set)

    for u, v, d in graph.edges(data=True):
        if not edge_has_annotation(d, annotation):
            continue

        result[d[ANNOTATIONS][annotation]].add(u)
        result[d[ANNOTATIONS][annotation]].add(v)

    return dict(result)