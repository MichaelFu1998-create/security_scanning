def random_by_edges(graph: BELGraph, percentage: Optional[float] = None) -> BELGraph:
    """Get a random graph by keeping a certain percentage of original edges.

    :param graph: A BEL graph
    :param percentage: What percentage of eges to take
    """
    percentage = percentage or 0.9
    assert 0 < percentage <= 1

    edges = graph.edges(keys=True)
    n = int(graph.number_of_edges() * percentage)

    subedges = random.sample(edges, n)

    rv = graph.fresh_copy()

    for u, v, k in subedges:
        safe_add_edge(rv, u, v, k, graph[u][v][k])

    update_node_helper(graph, rv)

    return rv