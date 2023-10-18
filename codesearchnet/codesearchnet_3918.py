def unique(items, key=None):
    """
    Generates unique items in the order they appear.

    Args:
        items (Iterable): list of items

        key (Callable, optional): custom normalization function.
            If specified returns items where `key(item)` is unique.

    Yields:
        object: a unique item from the input sequence

    CommandLine:
        python -m utool.util_list --exec-unique_ordered

    Example:
        >>> import ubelt as ub
        >>> items = [4, 6, 6, 0, 6, 1, 0, 2, 2, 1]
        >>> unique_items = list(ub.unique(items))
        >>> assert unique_items == [4, 6, 0, 1, 2]

    Example:
        >>> import ubelt as ub
        >>> items = ['A', 'a', 'b', 'B', 'C', 'c', 'D', 'e', 'D', 'E']
        >>> unique_items = list(ub.unique(items, key=six.text_type.lower))
        >>> assert unique_items == ['A', 'b', 'C', 'D', 'e']
        >>> unique_items = list(ub.unique(items))
        >>> assert unique_items == ['A', 'a', 'b', 'B', 'C', 'c', 'D', 'e', 'E']
    """
    seen = set()
    if key is None:
        for item in items:
            if item not in seen:
                seen.add(item)
                yield item
    else:
        for item in items:
            norm = key(item)
            if norm not in seen:
                seen.add(norm)
                yield item