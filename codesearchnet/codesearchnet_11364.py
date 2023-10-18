def gotoh(src, tar, gap_open=1, gap_ext=0.4, sim_func=sim_ident):
    """Return the Gotoh score of two strings.

    This is a wrapper for :py:meth:`Gotoh.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    gap_open : float
        The cost of an open alignment gap (1 by default)
    gap_ext : float
        The cost of an alignment gap extension (0.4 by default)
    sim_func : function
        A function that returns the similarity of two characters (identity
        similarity by default)

    Returns
    -------
    float
        Gotoh score

    Examples
    --------
    >>> gotoh('cat', 'hat')
    2.0
    >>> gotoh('Niall', 'Neil')
    1.0
    >>> round(gotoh('aluminum', 'Catalan'), 12)
    -0.4
    >>> gotoh('cat', 'hat')
    2.0

    """
    return Gotoh().dist_abs(src, tar, gap_open, gap_ext, sim_func)