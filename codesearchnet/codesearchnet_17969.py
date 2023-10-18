def delistify(a, b=None):
    """
    If a single element list, extract the element as an object, otherwise
    leave as it is.

    Examples
    --------
    >>> delistify('string')
    'string'

    >>> delistify(['string'])
    'string'

    >>> delistify(['string', 'other'])
    ['string', 'other']

    >>> delistify(np.array([1.0]))
    1.0

    >>> delistify([1, 2, 3])
    [1, 2, 3]
    """
    if isinstance(b, (tuple, list, np.ndarray)):
        if isinstance(a, (tuple, list, np.ndarray)):
            return type(b)(a)
        return type(b)([a])
    else:
        if isinstance(a, (tuple, list, np.ndarray)) and len(a) == 1:
            return a[0]
        return a
    return a