def _sort_itemstrs(items, itemstrs):
    """
    Equivalent to `sorted(items)` except if `items` are unorderable, then
    string values are used to define an ordering.
    """
    # First try to sort items by their normal values
    # If that doesnt work, then sort by their string values
    import ubelt as ub
    try:
        # Set ordering is not unique. Sort by strings values instead.
        if _peek_isinstance(items, (set, frozenset)):
            raise TypeError
        sortx = ub.argsort(items)
    except TypeError:
        sortx = ub.argsort(itemstrs)
    itemstrs = [itemstrs[x] for x in sortx]
    return itemstrs