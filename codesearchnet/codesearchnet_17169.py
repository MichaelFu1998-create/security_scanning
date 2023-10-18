def get_circulations(elements: T) -> Iterable[T]:
    """Iterate over all possible circulations of an ordered collection (tuple or list).

    Example:

    >>> list(get_circulations([1, 2, 3]))
    [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
    """
    for i in range(len(elements)):
        yield elements[i:] + elements[:i]