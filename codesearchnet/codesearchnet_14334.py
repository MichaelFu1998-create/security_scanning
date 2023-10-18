def precision(x):
    """
    Return the precision of x

    Parameters
    ----------
    x : array_like | numeric
        Value(s) whose for which to compute the precision.

    Returns
    -------
    out : numeric
        The precision of ``x`` or that the values in ``x``.

    Notes
    -----
    The precision is computed in base 10.

    Examples
    --------
    >>> precision(0.08)
    0.01
    >>> precision(9)
    1
    >>> precision(16)
    10
    """
    from .bounds import zero_range

    rng = min_max(x, na_rm=True)
    if zero_range(rng):
        span = np.abs(rng[0])
    else:
        span = np.diff(rng)[0]

    if span == 0:
        return 1
    else:
        return 10 ** int(np.floor(np.log10(span)))