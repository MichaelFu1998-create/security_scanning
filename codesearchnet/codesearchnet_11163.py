def sim_strcmp95(src, tar, long_strings=False):
    """Return the strcmp95 similarity of two strings.

    This is a wrapper for :py:meth:`Strcmp95.sim`.

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
        Strcmp95 similarity

    Examples
    --------
    >>> sim_strcmp95('cat', 'hat')
    0.7777777777777777
    >>> sim_strcmp95('Niall', 'Neil')
    0.8454999999999999
    >>> sim_strcmp95('aluminum', 'Catalan')
    0.6547619047619048
    >>> sim_strcmp95('ATCG', 'TAGC')
    0.8333333333333334

    """
    return Strcmp95().sim(src, tar, long_strings)