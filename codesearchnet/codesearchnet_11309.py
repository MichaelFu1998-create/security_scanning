def dist_editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the normalized Editex distance between two strings.

    This is a wrapper for :py:meth:`Editex.dist`.

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
        Normalized Editex distance

    Examples
    --------
    >>> round(dist_editex('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_editex('Niall', 'Neil'), 12)
    0.2
    >>> dist_editex('aluminum', 'Catalan')
    0.75
    >>> dist_editex('ATCG', 'TAGC')
    0.75

    """
    return Editex().dist(src, tar, cost, local)