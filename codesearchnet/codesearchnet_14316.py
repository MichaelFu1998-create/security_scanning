def rescale(x, to=(0, 1), _from=None):
    """
    Rescale numeric vector to have specified minimum and maximum.

    Parameters
    ----------
    x : array_like | numeric
        1D vector of values to manipulate.
    to : tuple
        output range (numeric vector of length two)
    _from : tuple
        input range (numeric vector of length two).
        If not given, is calculated from the range of x

    Returns
    -------
    out : array_like
        Rescaled values

    Examples
    --------
    >>> x = [0, 2, 4, 6, 8, 10]
    >>> rescale(x)
    array([0. , 0.2, 0.4, 0.6, 0.8, 1. ])
    >>> rescale(x, to=(0, 2))
    array([0. , 0.4, 0.8, 1.2, 1.6, 2. ])
    >>> rescale(x, to=(0, 2), _from=(0, 20))
    array([0. , 0.2, 0.4, 0.6, 0.8, 1. ])
    """
    if _from is None:
        _from = np.min(x), np.max(x)
    return np.interp(x, _from, to)