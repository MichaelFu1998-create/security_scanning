def sim_baystat(src, tar, min_ss_len=None, left_ext=None, right_ext=None):
    """Return the Baystat similarity.

    This is a wrapper for :py:meth:`Baystat.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    min_ss_len : int
        Minimum substring length to be considered
    left_ext :int
        Left-side extension length
    right_ext :int
        Right-side extension length

    Returns
    -------
    float
        The Baystat similarity

    Examples
    --------
    >>> round(sim_baystat('cat', 'hat'), 12)
    0.666666666667
    >>> sim_baystat('Niall', 'Neil')
    0.4
    >>> round(sim_baystat('Colin', 'Cuilen'), 12)
    0.166666666667
    >>> sim_baystat('ATCG', 'TAGC')
    0.0

    """
    return Baystat().sim(src, tar, min_ss_len, left_ext, right_ext)