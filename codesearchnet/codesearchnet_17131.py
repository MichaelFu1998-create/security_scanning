def count_sources(edge_iter: EdgeIterator) -> Counter:
    """Count the source nodes in an edge iterator with keys and data.

    :return: A counter of source nodes in the iterable
    """
    return Counter(u for u, _, _ in edge_iter)