def unique_flags(items, key=None):
    """
    Returns a list of booleans corresponding to the first instance of each
    unique item.

    Args:
        items (Sequence): indexable collection of items

        key (Callable, optional): custom normalization function.
            If specified returns items where `key(item)` is unique.

    Returns:
        List[bool] : flags the items that are unique

    Example:
        >>> import ubelt as ub
        >>> items = [0, 2, 1, 1, 0, 9, 2]
        >>> flags = unique_flags(items)
        >>> assert flags == [True, True, True, False, False, True, False]
        >>> flags = unique_flags(items, key=lambda x: x % 2 == 0)
        >>> assert flags == [True, False, True, False, False, False, False]
    """
    len_ = len(items)
    if key is None:
        item_to_index = dict(zip(reversed(items), reversed(range(len_))))
        indices = item_to_index.values()
    else:
        indices = argunique(items, key=key)
    flags = boolmask(indices, len_)
    return flags