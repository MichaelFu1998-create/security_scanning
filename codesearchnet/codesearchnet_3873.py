def _list_itemstrs(list_, **kwargs):
    """
    Create a string representation for each item in a list.
    """
    items = list(list_)
    kwargs['_return_info'] = True
    _tups = [repr2(item, **kwargs) for item in items]
    itemstrs = [t[0] for t in _tups]
    max_height = max([t[1]['max_height'] for t in _tups]) if _tups else 0
    _leaf_info = {
        'max_height': max_height + 1,
    }

    sort = kwargs.get('sort', None)
    if sort is None:
        # Force orderings on sets.
        sort = isinstance(list_, (set, frozenset))
    if sort:
        itemstrs = _sort_itemstrs(items, itemstrs)
    return itemstrs, _leaf_info