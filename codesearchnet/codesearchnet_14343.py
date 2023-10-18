def area_pal(range=(1, 6)):
    """
    Point area palette (continuous).

    Parameters
    ----------
    range : tuple
        Numeric vector of length two, giving range of possible sizes.
        Should be greater than 0.

    Returns
    -------
    out : function
        Palette function that takes a sequence of values
        in the range ``[0, 1]`` and returns values in
        the specified range.

    Examples
    --------
    >>> x = np.arange(0, .6, .1)**2
    >>> palette = area_pal()
    >>> palette(x)
    array([1. , 1.5, 2. , 2.5, 3. , 3.5])

    The results are equidistant because the input ``x`` is in
    area space, i.e it is squared.
    """
    def area_palette(x):
        return rescale(np.sqrt(x), to=range, _from=(0, 1))
    return area_palette