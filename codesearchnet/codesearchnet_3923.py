def argsort(indexable, key=None, reverse=False):
    """
    Returns the indices that would sort a indexable object.

    This is similar to `numpy.argsort`, but it is written in pure python and
    works on both lists and dictionaries.

    Args:
        indexable (Iterable or Mapping): indexable to sort by

        key (Callable, optional): customizes the ordering of the indexable

        reverse (bool, optional): if True returns in descending order

    Returns:
        list: indices: list of indices such that sorts the indexable

    Example:
        >>> import ubelt as ub
        >>> # argsort works on dicts by returning keys
        >>> dict_ = {'a': 3, 'b': 2, 'c': 100}
        >>> indices = ub.argsort(dict_)
        >>> assert list(ub.take(dict_, indices)) == sorted(dict_.values())
        >>> # argsort works on lists by returning indices
        >>> indexable = [100, 2, 432, 10]
        >>> indices = ub.argsort(indexable)
        >>> assert list(ub.take(indexable, indices)) == sorted(indexable)
        >>> # Can use iterators, but be careful. It exhausts them.
        >>> indexable = reversed(range(100))
        >>> indices = ub.argsort(indexable)
        >>> assert indices[0] == 99
        >>> # Can use key just like sorted
        >>> indexable = [[0, 1, 2], [3, 4], [5]]
        >>> indices = ub.argsort(indexable, key=len)
        >>> assert indices == [2, 1, 0]
        >>> # Can use reverse just like sorted
        >>> indexable = [0, 2, 1]
        >>> indices = ub.argsort(indexable, reverse=True)
        >>> assert indices == [1, 2, 0]
    """
    # Create an iterator of value/key pairs
    if isinstance(indexable, collections_abc.Mapping):
        vk_iter = ((v, k) for k, v in indexable.items())
    else:
        vk_iter = ((v, k) for k, v in enumerate(indexable))
    # Sort by values and extract the indices
    if key is None:
        indices = [k for v, k in sorted(vk_iter, reverse=reverse)]
    else:
        # If key is provided, call it using the value as input
        indices = [k for v, k in sorted(vk_iter, key=lambda vk: key(vk[0]),
                                        reverse=reverse)]
    return indices