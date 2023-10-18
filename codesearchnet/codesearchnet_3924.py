def argmax(indexable, key=None):
    """
    Returns index / key of the item with the largest value.

    This is similar to `numpy.argmax`, but it is written in pure python and
    works on both lists and dictionaries.

    Args:
        indexable (Iterable or Mapping): indexable to sort by

        key (Callable, optional): customizes the ordering of the indexable

    CommandLine:
        python -m ubelt.util_list argmax

    Example:
        >>> assert argmax({'a': 3, 'b': 2, 'c': 100}) == 'c'
        >>> assert argmax(['a', 'c', 'b', 'z', 'f']) == 3
        >>> assert argmax([[0, 1], [2, 3, 4], [5]], key=len) == 1
        >>> assert argmax({'a': 3, 'b': 2, 3: 100, 4: 4}) == 3
        >>> assert argmax(iter(['a', 'c', 'b', 'z', 'f'])) == 3
    """
    if key is None and isinstance(indexable, collections_abc.Mapping):
        return max(indexable.items(), key=operator.itemgetter(1))[0]
    elif hasattr(indexable, 'index'):
        if key is None:
            return indexable.index(max(indexable))
        else:
            return indexable.index(max(indexable, key=key))
    else:
        # less efficient, but catch all solution
        return argsort(indexable, key=key)[-1]