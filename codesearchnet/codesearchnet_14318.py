def rescale_max(x, to=(0, 1), _from=None):
    """
    Rescale numeric vector to have specified maximum.

    Parameters
    ----------
    x : array_like | numeric
        1D vector of values to manipulate.
    to : tuple
        output range (numeric vector of length two)
    _from : tuple
        input range (numeric vector of length two).
        If not given, is calculated from the range of x.
        Only the 2nd (max) element is essential to the
        output.

    Returns
    -------
    out : array_like
        Rescaled values

    Examples
    --------
    >>> x = [0, 2, 4, 6, 8, 10]
    >>> rescale_max(x, (0, 3))
    array([0. , 0.6, 1.2, 1.8, 2.4, 3. ])

    Only the 2nd (max) element of the parameters ``to``
    and ``_from`` are essential to the output.

    >>> rescale_max(x, (1, 3))
    array([0. , 0.6, 1.2, 1.8, 2.4, 3. ])
    >>> rescale_max(x, (0, 20))
    array([ 0.,  4.,  8., 12., 16., 20.])

    If :python:`max(x) < _from[1]` then values will be
    scaled beyond the requested (:python:`to[1]`) maximum.

    >>> rescale_max(x, to=(1, 3), _from=(-1, 6))
    array([0., 1., 2., 3., 4., 5.])

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

    out = x/_from[1] * to[1]

    if not array_like:
        out = out[0]
    return out