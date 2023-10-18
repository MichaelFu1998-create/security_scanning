def dist_monge_elkan(src, tar, sim_func=sim_levenshtein, symmetric=False):
    """Return the Monge-Elkan distance between two strings.

    This is a wrapper for :py:meth:`MongeElkan.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    sim_func : function
        The internal similarity metric to employ
    symmetric : bool
        Return a symmetric similarity measure

    Returns
    -------
    float
        Monge-Elkan distance

    Examples
    --------
    >>> dist_monge_elkan('cat', 'hat')
    0.25
    >>> round(dist_monge_elkan('Niall', 'Neil'), 12)
    0.333333333333
    >>> round(dist_monge_elkan('aluminum', 'Catalan'), 12)
    0.611111111111
    >>> dist_monge_elkan('ATCG', 'TAGC')
    0.5

    """
    return MongeElkan().dist(src, tar, sim_func, symmetric)