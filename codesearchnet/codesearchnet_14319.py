def squish_infinite(x, range=(0, 1)):
    """
    Truncate infinite values to a range.

    Parameters
    ----------
    x : array_like
        Values that should have infinities squished.
    range : tuple
        The range onto which to squish the infinites.
        Must be of size 2.

    Returns
    -------
    out : array_like
        Values with infinites squished.

    Examples
    --------
    >>> squish_infinite([0, .5, .25, np.inf, .44])
    [0.0, 0.5, 0.25, 1.0, 0.44]
    >>> squish_infinite([0, -np.inf, .5, .25, np.inf], (-10, 9))
    [0.0, -10.0, 0.5, 0.25, 9.0]
    """
    xtype = type(x)

    if not hasattr(x, 'dtype'):
        x = np.asarray(x)

    x[x == -np.inf] = range[0]
    x[x == np.inf] = range[1]

    if not isinstance(x, xtype):
        x = xtype(x)
    return x