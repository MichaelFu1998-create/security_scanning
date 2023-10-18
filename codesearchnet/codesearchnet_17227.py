def shuffle_relations(graph: BELGraph, percentage: Optional[str] = None) -> BELGraph:
    """Shuffle the relations.

    Useful for permutation testing.

    :param graph: A BEL graph
    :param percentage: What percentage of possible swaps to make
    """
    percentage = percentage or 0.3
    assert 0 < percentage <= 1

    n = graph.number_of_edges()
    swaps = int(percentage * n * (n - 1) / 2)

    result: BELGraph = graph.copy()

    edges = result.edges(keys=True)

    for _ in range(swaps):
        (s1, t1, k1), (s2, t2, k2) = random.sample(edges, 2)
        result[s1][t1][k1], result[s2][t2][k2] = result[s2][t2][k2], result[s1][t1][k1]

    return result