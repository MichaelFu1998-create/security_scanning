def dzip(items1, items2, cls=dict):
    """
    Zips elementwise pairs between items1 and items2 into a dictionary. Values
    from items2 can be broadcast onto items1.

    Args:
        items1 (Iterable): full sequence
        items2 (Iterable): can either be a sequence of one item or a sequence
            of equal length to `items1`
        cls (Type[dict]): dictionary type to use. Defaults to dict, but could
            be ordered dict instead.

    Returns:
        dict: similar to dict(zip(items1, items2))

    Example:
        >>> assert dzip([1, 2, 3], [4]) == {1: 4, 2: 4, 3: 4}
        >>> assert dzip([1, 2, 3], [4, 4, 4]) == {1: 4, 2: 4, 3: 4}
        >>> assert dzip([], [4]) == {}
    """
    try:
        len(items1)
    except TypeError:
        items1 = list(items1)
    try:
        len(items2)
    except TypeError:
        items2 = list(items2)
    if len(items1) == 0 and len(items2) == 1:
        # Corner case:
        # allow the first list to be empty and the second list to broadcast a
        # value. This means that the equality check wont work for the case
        # where items1 and items2 are supposed to correspond, but the length of
        # items2 is 1.
        items2 = []
    if len(items2) == 1 and len(items1) > 1:
        items2 = items2 * len(items1)
    if len(items1) != len(items2):
        raise ValueError('out of alignment len(items1)=%r, len(items2)=%r' % (
            len(items1), len(items2)))
    return cls(zip(items1, items2))