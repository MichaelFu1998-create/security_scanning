def sim_editex(src, tar, cost=(0, 1, 2), local=False):
    """Return the normalized Editex similarity of two strings.

    This is a wrapper for :py:meth:`Editex.sim`.

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
        Normalized Editex similarity

    Examples
    --------
    >>> round(sim_editex('cat', 'hat'), 12)
    0.666666666667
    >>> round(sim_editex('Niall', 'Neil'), 12)
    0.8
    >>> sim_editex('aluminum', 'Catalan')
    0.25
    >>> sim_editex('ATCG', 'TAGC')
    0.25

    """
    return Editex().sim(src, tar, cost, local)