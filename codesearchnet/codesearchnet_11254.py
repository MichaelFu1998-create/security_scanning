def smith_waterman(src, tar, gap_cost=1, sim_func=sim_ident):
    """Return the Smith-Waterman score of two strings.

    This is a wrapper for :py:meth:`SmithWaterman.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    gap_cost : float
        The cost of an alignment gap (1 by default)
    sim_func : function
        A function that returns the similarity of two characters (identity
        similarity by default)

    Returns
    -------
    float
        Smith-Waterman score

    Examples
    --------
    >>> smith_waterman('cat', 'hat')
    2.0
    >>> smith_waterman('Niall', 'Neil')
    1.0
    >>> smith_waterman('aluminum', 'Catalan')
    0.0
    >>> smith_waterman('ATCG', 'TAGC')
    1.0

    """
    return SmithWaterman().dist_abs(src, tar, gap_cost, sim_func)