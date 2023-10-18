def rescale_mid(x, to=(0, 1), _from=None, mid=0):
    """
    Rescale numeric vector to have specified minimum, midpoint,
    and maximum.

    Parameters
    ----------
    x : array_like | numeric
        1D vector of values to manipulate.
    to : tuple
        output range (numeric vector of length two)
    _from : tuple
        input range (numeric vector of length two).
        If not given, is calculated from the range of x
    mid	: numeric
        mid-point of input range

    Returns
    -------
    out : array_like
        Rescaled values

    Examples
    --------
    >>> rescale_mid([1, 2, 3], mid=1)
    array([0.5 , 0.75, 1.  ])
    >>> rescale_mid([1, 2, 3], mid=2)
    array([0. , 0.5, 1. ])
    """
    array_like = True

    try:
        len(x)
    except TypeError:
        array_like = False
        x = [x]

    if not hasattr(x, 'dtype'):
        x = np.asarray(x)

    if _from is None:
        _from = np.array([np.min(x), np.max(x)])
    else:
        _from = np.asarray(_from)

    if (zero_range(_from) or zero_range(to)):
        out = np.repeat(np.mean(to), len(x))
    else:
        extent = 2 * np.max(np.abs(_from - mid))
        out = (x - mid) / extent * np.diff(to) + np.mean(to)

    if not array_like:
        out = out[0]
    return out