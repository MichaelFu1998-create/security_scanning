def enrich_internal_unqualified_edges(graph, subgraph):
    """Add the missing unqualified edges between entities in the subgraph that are contained within the full graph.

    :param pybel.BELGraph graph: The full BEL graph
    :param pybel.BELGraph subgraph: The query BEL subgraph
    """
    for u, v in itt.combinations(subgraph, 2):
        if not graph.has_edge(u, v):
            continue

        for k in graph[u][v]:
            if k < 0:
                subgraph.add_edge(u, v, key=k, **graph[u][v][k])