def sim_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Return the Monge-Elkan similarity of two strings.

    This is a wrapper for :py:meth:`MongeElkan.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    sim_func : function
        Rhe internal similarity metric to employ
    symmetric : bool
        Return a symmetric similarity measure

    Returns
    -------
    float
        Monge-Elkan similarity

    Examples
    --------
    >>> sim_monge_elkan('cat', 'hat')
    0.75
    >>> round(sim_monge_elkan('Niall', 'Neil'), 12)
    0.666666666667
    >>> round(sim_monge_elkan('aluminum', 'Catalan'), 12)
    0.388888888889
    >>> sim_monge_elkan('ATCG', 'TAGC')
    0.5

    """
    return MongeElkan().sim(src, tar, sim_func, symmetric)