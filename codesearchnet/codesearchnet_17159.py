def min_tanimoto_set_similarity(x: Iterable[X], y: Iterable[X]) -> float:
    """Calculate the tanimoto set similarity using the minimum size.

    :param set x: A set
    :param set y: Another set
    :return: The similarity between
        """
    a, b = set(x), set(y)

    if not a or not b:
        return 0.0

    return len(a & b) / min(len(a), len(b))