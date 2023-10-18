def expand_range(range, mul=0, add=0, zero_width=1):
    """
    Expand a range with a multiplicative or additive constant

    Parameters
    ----------
    range : tuple
        Range of data. Size 2.
    mul : int | float
        Multiplicative constant
    add : int | float | timedelta
        Additive constant
    zero_width : int | float | timedelta
        Distance to use if range has zero width

    Returns
    -------
    out : tuple
        Expanded range

    Examples
    --------
    >>> expand_range((3, 8))
    (3, 8)
    >>> expand_range((0, 10), mul=0.1)
    (-1.0, 11.0)
    >>> expand_range((0, 10), add=2)
    (-2, 12)
    >>> expand_range((0, 10), mul=.1, add=2)
    (-3.0, 13.0)
    >>> expand_range((0, 1))
    (0, 1)

    When the range has zero width

    >>> expand_range((5, 5))
    (4.5, 5.5)

    Notes
    -----
    If expanding *datetime* or *timedelta* types, **add** and
    **zero_width** must be suitable *timedeltas* i.e. You should
    not mix types between **Numpy**, **Pandas** and the
    :mod:`datetime` module.

    In Python 2, you cannot multiplicative constant **mul** cannot be
    a :class:`float`.
    """
    x = range

    # Enforce tuple
    try:
        x[0]
    except TypeError:
        x = (x, x)

    # The expansion cases
    if zero_range(x):
        new = x[0]-zero_width/2, x[0]+zero_width/2
    else:
        dx = (x[1] - x[0]) * mul + add
        new = x[0]-dx, x[1]+dx

    return new