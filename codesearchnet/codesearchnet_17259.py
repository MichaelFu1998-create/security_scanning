def remove_inconsistent_edges(graph: BELGraph) -> None:
    """Remove all edges between node pairs with inconsistent edges.

    This is the all-or-nothing approach. It would be better to do more careful investigation of the evidences during
    curation.
    """
    for u, v in get_inconsistent_edges(graph):
        edges = [(u, v, k) for k in graph[u][v]]
        graph.remove_edges_from(edges)