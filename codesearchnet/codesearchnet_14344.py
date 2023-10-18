def abs_area(max):
    """
    Point area palette (continuous), with area proportional to value.

    Parameters
    ----------
    max : float
        A number representing the maximum size

    Returns
    -------
    out : function
        Palette function that takes a sequence of values
        in the range ``[0, 1]`` and returns values in the range
        ``[0, max]``.

    Examples
    --------
    >>> x = np.arange(0, .8, .1)**2
    >>> palette = abs_area(5)
    >>> palette(x)
    array([0. , 0.5, 1. , 1.5, 2. , 2.5, 3. , 3.5])

    Compared to :func:`area_pal`, :func:`abs_area` will handle values
    in the range ``[-1, 0]`` without returning ``np.nan``. And values
    whose absolute value is greater than 1 will be clipped to the
    maximum.
    """
    def abs_area_palette(x):
        return rescale(np.sqrt(np.abs(x)), to=(0, max), _from=(0, 1))
    return abs_area_palette