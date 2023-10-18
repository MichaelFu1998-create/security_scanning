def argunique(items, key=None):
    """
    Returns indices corresponding to the first instance of each unique item.

    Args:
        items (Sequence): indexable collection of items

        key (Callable, optional): custom normalization function.
            If specified returns items where `key(item)` is unique.

    Yields:
        int : indices of the unique items

    Example:
        >>> items = [0, 2, 5, 1, 1, 0, 2, 4]
        >>> indices = list(argunique(items))
        >>> assert indices == [0, 1, 2, 3, 7]
        >>> indices = list(argunique(items, key=lambda x: x % 2 == 0))
        >>> assert indices == [0, 2]
    """
    # yield from unique(range(len(items)), key=lambda i: items[i])
    if key is None:
        return unique(range(len(items)), key=lambda i: items[i])
    else:
        return unique(range(len(items)), key=lambda i: key(items[i]))