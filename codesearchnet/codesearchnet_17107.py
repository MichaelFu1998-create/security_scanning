def collapse_consistent_edges(graph: BELGraph):
    """Collapse consistent edges together.

    .. warning:: This operation doesn't preserve evidences or other annotations
    """
    for u, v in graph.edges():
        relation = pair_is_consistent(graph, u, v)

        if not relation:
            continue

        edges = [(u, v, k) for k in graph[u][v]]
        graph.remove_edges_from(edges)
        graph.add_edge(u, v, attr_dict={RELATION: relation})