def sim_minkowski(src, tar, qval=2, pval=1, alphabet=None):
    """Return normalized Minkowski similarity of two strings.

    This is a wrapper for :py:meth:`Minkowski.sim`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    pval : int or float
        The :math:`p`-value of the :math:`L^p`-space
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The normalized Minkowski similarity

    Examples
    --------
    >>> sim_minkowski('cat', 'hat')
    0.5
    >>> round(sim_minkowski('Niall', 'Neil'), 12)
    0.363636363636
    >>> round(sim_minkowski('Colin', 'Cuilen'), 12)
    0.307692307692
    >>> sim_minkowski('ATCG', 'TAGC')
    0.0

    """
    return Minkowski().sim(src, tar, qval, pval, alphabet)