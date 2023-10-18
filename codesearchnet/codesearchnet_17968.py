def listify(a):
    """
    Convert a scalar ``a`` to a list and all iterables to list as well.

    Examples
    --------
    >>> listify(0)
    [0]

    >>> listify([1,2,3])
    [1, 2, 3]

    >>> listify('a')
    ['a']

    >>> listify(np.array([1,2,3]))
    [1, 2, 3]

    >>> listify('string')
    ['string']
    """
    if a is None:
        return []
    elif not isinstance(a, (tuple, list, np.ndarray)):
        return [a]
    return list(a)