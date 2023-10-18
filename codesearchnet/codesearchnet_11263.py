def dist_minkowski(src, tar, qval=2, pval=1, alphabet=None):
    """Return normalized Minkowski distance of two strings.

    This is a wrapper for :py:meth:`Minkowski.dist`.

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
        The normalized Minkowski distance

    Examples
    --------
    >>> dist_minkowski('cat', 'hat')
    0.5
    >>> round(dist_minkowski('Niall', 'Neil'), 12)
    0.636363636364
    >>> round(dist_minkowski('Colin', 'Cuilen'), 12)
    0.692307692308
    >>> dist_minkowski('ATCG', 'TAGC')
    1.0

    """
    return Minkowski().dist(src, tar, qval, pval, alphabet)