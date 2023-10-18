def zero_range(x, tol=np.finfo(float).eps * 100):
    """
    Determine if range of vector is close to zero.

    Parameters
    ----------
    x : array_like | numeric
        Value(s) to check. If it is an array_like, it
        should be of length 2.
    tol : float
        Tolerance. Default tolerance is the `machine epsilon`_
        times :math:`10^2`.

    Returns
    -------
    out : bool
        Whether ``x`` has zero range.

    Examples
    --------
    >>> zero_range([1, 1])
    True
    >>> zero_range([1, 2])
    False
    >>> zero_range([1, 2], tol=2)
    True

    .. _machine epsilon: https://en.wikipedia.org/wiki/Machine_epsilon
    """
    try:
        if len(x) == 1:
            return True
    except TypeError:
        return True

    if len(x) != 2:
        raise ValueError('x must be length 1 or 2')

    # Deals with array_likes that have non-standard indices
    x = tuple(x)

    # datetime - pandas, cpython
    if isinstance(x[0], (pd.Timestamp, datetime.datetime)):
        # date2num include timezone info, .toordinal() does not
        x = date2num(x)
    # datetime - numpy
    elif isinstance(x[0], np.datetime64):
        return x[0] == x[1]
    # timedelta - pandas, cpython
    elif isinstance(x[0], (pd.Timedelta, datetime.timedelta)):
        x = x[0].total_seconds(), x[1].total_seconds()
    # timedelta - numpy
    elif isinstance(x[0], np.timedelta64):
        return x[0] == x[1]
    elif not isinstance(x[0], (float, int, np.number)):
        raise TypeError(
            "zero_range objects cannot work with objects "
            "of type '{}'".format(type(x[0])))

    if any(np.isnan(x)):
        return np.nan

    if x[0] == x[1]:
        return True

    if all(np.isinf(x)):
        return False

    m = np.abs(x).min()
    if m == 0:
        return False

    return np.abs((x[0] - x[1]) / m) < tol