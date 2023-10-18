def argmin(indexable, key=None):
    """
    Returns index / key of the item with the smallest value.

    This is similar to `numpy.argmin`, but it is written in pure python and
    works on both lists and dictionaries.

    Args:
        indexable (Iterable or Mapping): indexable to sort by

        key (Callable, optional): customizes the ordering of the indexable

    Example:
        >>> assert argmin({'a': 3, 'b': 2, 'c': 100}) == 'b'
        >>> assert argmin(['a', 'c', 'b', 'z', 'f']) == 0
        >>> assert argmin([[0, 1], [2, 3, 4], [5]], key=len) == 2
        >>> assert argmin({'a': 3, 'b': 2, 3: 100, 4: 4}) == 'b'
        >>> assert argmin(iter(['a', 'c', 'A', 'z', 'f'])) == 2
    """
    if key is None and isinstance(indexable, collections_abc.Mapping):
        return min(indexable.items(), key=operator.itemgetter(1))[0]
    elif hasattr(indexable, 'index'):
        if key is None:
            return indexable.index(min(indexable))
        else:
            return indexable.index(min(indexable, key=key))
    else:
        # less efficient, but catch all solution
        return argsort(indexable, key=key)[0]