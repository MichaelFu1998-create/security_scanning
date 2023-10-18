def dist_baystat(src, tar, min_ss_len=None, left_ext=None, right_ext=None):
    """Return the Baystat distance.

    This is a wrapper for :py:meth:`Baystat.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    min_ss_len : int
        Minimum substring length to be considered
    left_ext : int
        Left-side extension length
    right_ext : int
        Right-side extension length

    Returns
    -------
    float
        The Baystat distance

    Examples
    --------
    >>> round(dist_baystat('cat', 'hat'), 12)
    0.333333333333
    >>> dist_baystat('Niall', 'Neil')
    0.6
    >>> round(dist_baystat('Colin', 'Cuilen'), 12)
    0.833333333333
    >>> dist_baystat('ATCG', 'TAGC')
    1.0

    """
    return Baystat().dist(src, tar, min_ss_len, left_ext, right_ext)