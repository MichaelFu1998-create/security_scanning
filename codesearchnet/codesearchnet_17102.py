def _collapse_edge_passing_predicates(graph: BELGraph, edge_predicates: EdgePredicates = None) -> None:
    """Collapse all edges passing the given edge predicates."""
    for u, v, _ in filter_edges(graph, edge_predicates=edge_predicates):
        collapse_pair(graph, survivor=u, victim=v)