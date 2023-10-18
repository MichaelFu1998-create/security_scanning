def random_by_nodes(graph: BELGraph, percentage: Optional[float] = None) -> BELGraph:
    """Get a random graph by inducing over a percentage of the original nodes.

    :param graph: A BEL graph
    :param percentage: The percentage of edges to keep
    """
    percentage = percentage or 0.9

    assert 0 < percentage <= 1

    nodes = graph.nodes()
    n = int(len(nodes) * percentage)

    subnodes = random.sample(nodes, n)

    result = graph.subgraph(subnodes)

    update_node_helper(graph, result)

    return result