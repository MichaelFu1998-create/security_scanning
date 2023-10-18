def calculate_betweenness_centality(graph: BELGraph, number_samples: int = CENTRALITY_SAMPLES) -> Counter:
    """Calculate the betweenness centrality over nodes in the graph.

    Tries to do it with a certain number of samples, but then tries a complete approach if it fails.
    """
    try:
        res = nx.betweenness_centrality(graph, k=number_samples)
    except Exception:
        res = nx.betweenness_centrality(graph)
    return Counter(res)