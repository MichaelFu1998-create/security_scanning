def dist_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 distance between two strings.

    This is a wrapper for :py:meth:`Strcmp95.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    long_strings : bool
        Set to True to increase the probability of a match when the number of
        matched characters is large. This option allows for a little more
        tolerance when the strings are large. It is not an appropriate test
        when comparing fixed length fields such as phone and social security
        numbers.

    Returns
    -------
    float
        Strcmp95 distance

    Examples
    --------
    >>> round(dist_strcmp95('cat', 'hat'), 12)
    0.222222222222
    >>> round(dist_strcmp95('Niall', 'Neil'), 12)
    0.1545
    >>> round(dist_strcmp95('aluminum', 'Catalan'), 12)
    0.345238095238
    >>> round(dist_strcmp95('ATCG', 'TAGC'), 12)
    0.166666666667

    """
    return Strcmp95().dist(src, tar, long_strings)