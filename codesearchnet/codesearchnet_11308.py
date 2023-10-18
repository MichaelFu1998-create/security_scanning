def editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the Editex distance between two strings.

    This is a wrapper for :py:meth:`Editex.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    cost : tuple
        A 3-tuple representing the cost of the four possible edits: match,
        same-group, and mismatch respectively (by default: (0, 1, 2))
    local : bool
        If True, the local variant of Editex is used

    Returns
    -------
    int
        Editex distance

    Examples
    --------
    >>> editex('cat', 'hat')
    2
    >>> editex('Niall', 'Neil')
    2
    >>> editex('aluminum', 'Catalan')
    12
    >>> editex('ATCG', 'TAGC')
    6

    """
    return Editex().dist_abs(src, tar, cost, local)