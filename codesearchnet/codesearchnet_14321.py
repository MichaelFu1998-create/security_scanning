def censor(x, range=(0, 1), only_finite=True):
    """
    Convert any values outside of range to a **NULL** type object.

    Parameters
    ----------
    x : array_like
        Values to manipulate
    range : tuple
        (min, max) giving desired output range
    only_finite : bool
        If True (the default), will only modify
        finite values.

    Returns
    -------
    x : array_like
        Censored array

    Examples
    --------
    >>> a = [1, 2, np.inf, 3, 4, -np.inf, 5]
    >>> censor(a, (0, 10))
    [1, 2, inf, 3, 4, -inf, 5]
    >>> censor(a, (0, 10), False)
    [1, 2, nan, 3, 4, nan, 5]
    >>> censor(a, (2, 4))
    [nan, 2, inf, 3, 4, -inf, nan]

    Notes
    -----
    All values in ``x`` should be of the same type. ``only_finite`` parameter
    is not considered for Datetime and Timedelta types.

    The **NULL** type object depends on the type of values in **x**.

    - :class:`float` - :py:`float('nan')`
    - :class:`int` - :py:`float('nan')`
    - :class:`datetime.datetime` : :py:`np.datetime64(NaT)`
    - :class:`datetime.timedelta` : :py:`np.timedelta64(NaT)`

    """
    if not len(x):
        return x

    py_time_types = (datetime.datetime, datetime.timedelta)
    np_pd_time_types = (pd.Timestamp, pd.Timedelta,
                        np.datetime64, np.timedelta64)
    x0 = first_element(x)

    # Yes, we want type not isinstance
    if type(x0) in py_time_types:
        return _censor_with(x, range, 'NaT')

    if not hasattr(x, 'dtype') and isinstance(x0, np_pd_time_types):
        return _censor_with(x, range, type(x0)('NaT'))

    x_array = np.asarray(x)
    if pdtypes.is_number(x0) and not isinstance(x0, np.timedelta64):
        null = float('nan')
    elif com.is_datetime_arraylike(x_array):
        null = pd.Timestamp('NaT')
    elif pdtypes.is_datetime64_dtype(x_array):
        null = np.datetime64('NaT')
    elif isinstance(x0, pd.Timedelta):
        null = pd.Timedelta('NaT')
    elif pdtypes.is_timedelta64_dtype(x_array):
        null = np.timedelta64('NaT')
    else:
        raise ValueError(
            "Do not know how to censor values of type "
            "{}".format(type(x0)))

    if only_finite:
        try:
            finite = np.isfinite(x)
        except TypeError:
            finite = np.repeat(True, len(x))
    else:
        finite = np.repeat(True, len(x))

    if hasattr(x, 'dtype'):
        outside = (x < range[0]) | (x > range[1])
        bool_idx = finite & outside
        x = x.copy()
        x[bool_idx] = null
    else:
        x = [null if not range[0] <= val <= range[1] and f else val
             for val, f in zip(x, finite)]

    return x