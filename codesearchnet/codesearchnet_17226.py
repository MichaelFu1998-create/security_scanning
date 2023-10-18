def shuffle_node_data(graph: BELGraph, key: str, percentage: Optional[float] = None) -> BELGraph:
    """Shuffle the node's data.

    Useful for permutation testing.

    :param graph: A BEL graph
    :param key: The node data dictionary key
    :param percentage: What percentage of possible swaps to make
    """
    percentage = percentage or 0.3
    assert 0 < percentage <= 1

    n = graph.number_of_nodes()
    swaps = int(percentage * n * (n - 1) / 2)

    result: BELGraph = graph.copy()

    for _ in range(swaps):
        s, t = random.sample(result.node, 2)
        result.nodes[s][key], result.nodes[t][key] = result.nodes[t][key], result.nodes[s][key]

    return result