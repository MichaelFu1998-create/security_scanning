def dict_union(*args):
    """
    Combines the disjoint keys in multiple dictionaries. For intersecting keys,
    dictionaries towards the end of the sequence are given precedence.

    Args:
        *args : a sequence of dictionaries

    Returns:
        Dict | OrderedDict :
            OrderedDict if the first argument is an OrderedDict, otherwise dict

    SeeAlso:
        collections.ChainMap - a standard python builtin data structure that
            provides a view that treats multiple dicts as a single dict.
            https://docs.python.org/3/library/collections.html#chainmap-objects

    Example:
        >>> result = dict_union({'a': 1, 'b': 1}, {'b': 2, 'c': 2})
        >>> assert result == {'a': 1, 'b': 2, 'c': 2}
        >>> dict_union(odict([('a', 1), ('b', 2)]), odict([('c', 3), ('d', 4)]))
        OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4)])
        >>> dict_union()
        {}
    """
    if not args:
        return {}
    else:
        dictclass = OrderedDict if isinstance(args[0], OrderedDict) else dict
        return dictclass(it.chain.from_iterable(d.items() for d in args))