def squish(x, range=(0, 1), only_finite=True):
    """
    Squish values into range.

    Parameters
    ----------
    x : array_like
        Values that should have out of range values squished.
    range : tuple
        The range onto which to squish the values.
    only_finite: boolean
        When true, only squishes finite values.

    Returns
    -------
    out : array_like
        Values with out of range values squished.

    Examples
    --------
    >>> squish([-1.5, 0.2, 0.5, 0.8, 1.0, 1.2])
    [0.0, 0.2, 0.5, 0.8, 1.0, 1.0]

    >>> squish([-np.inf, -1.5, 0.2, 0.5, 0.8, 1.0, np.inf], only_finite=False)
    [0.0, 0.0, 0.2, 0.5, 0.8, 1.0, 1.0]
    """
    xtype = type(x)

    if not hasattr(x, 'dtype'):
        x = np.asarray(x)

    finite = np.isfinite(x) if only_finite else True

    x[np.logical_and(x < range[0], finite)] = range[0]
    x[np.logical_and(x > range[1], finite)] = range[1]

    if not isinstance(x, xtype):
        x = xtype(x)
    return x