def count_targets(edge_iter: EdgeIterator) -> Counter:
    """Count the target nodes in an edge iterator with keys and data.

    :return: A counter of target nodes in the iterable
    """
    return Counter(v for _, v, _ in edge_iter)