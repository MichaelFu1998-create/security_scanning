def dist_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS distance between two strings.

    This is a wrapper for :py:meth:`MLIPNS.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    threshold : float
        A number [0, 1] indicating the maximum similarity score, below which
        the strings are considered 'similar' (0.25 by default)
    max_mismatches : int
        A number indicating the allowable number of mismatches to remove before
        declaring two strings not similar (2 by default)

    Returns
    -------
    float
        MLIPNS distance

    Examples
    --------
    >>> dist_mlipns('cat', 'hat')
    0.0
    >>> dist_mlipns('Niall', 'Neil')
    1.0
    >>> dist_mlipns('aluminum', 'Catalan')
    1.0
    >>> dist_mlipns('ATCG', 'TAGC')
    1.0

    """
    return MLIPNS().dist(src, tar, threshold, max_mismatches)