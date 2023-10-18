def sim_mlipns(src, tar, threshold=0.25, max_mismatches=2):
    """Return the MLIPNS similarity of two strings.

    This is a wrapper for :py:meth:`MLIPNS.sim`.

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
        MLIPNS similarity

    Examples
    --------
    >>> sim_mlipns('cat', 'hat')
    1.0
    >>> sim_mlipns('Niall', 'Neil')
    0.0
    >>> sim_mlipns('aluminum', 'Catalan')
    0.0
    >>> sim_mlipns('ATCG', 'TAGC')
    0.0

    """
    return MLIPNS().sim(src, tar, threshold, max_mismatches)