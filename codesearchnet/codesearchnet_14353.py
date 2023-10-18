def manual_pal(values):
    """
    Create a palette from a list of values

    Parameters
    ----------
    values : sequence
        Values that will be returned by the palette function.

    Returns
    -------
    out : function
        A function palette that takes a single
        :class:`int` parameter ``n`` and returns ``n`` values.

    Examples
    --------
    >>> palette = manual_pal(['a', 'b', 'c', 'd', 'e'])
    >>> palette(3)
    ['a', 'b', 'c']
    """
    max_n = len(values)

    def _manual_pal(n):
        if n > max_n:
            msg = ("Palette can return a maximum of {} values. "
                   "{} were requested from it.")
            warnings.warn(msg.format(max_n, n))

        return values[:n]

    return _manual_pal