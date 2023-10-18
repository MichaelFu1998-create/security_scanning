def dist_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tversky distance between two strings.

    This is a wrapper for :py:meth:`Tversky.dist`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version
    alpha : float
        Tversky index parameter as described above
    beta : float
        Tversky index parameter as described above
    bias : float
        The symmetric Tversky index bias parameter

    Returns
    -------
    float
        Tversky distance

    Examples
    --------
    >>> dist_tversky('cat', 'hat')
    0.6666666666666667
    >>> dist_tversky('Niall', 'Neil')
    0.7777777777777778
    >>> dist_tversky('aluminum', 'Catalan')
    0.9375
    >>> dist_tversky('ATCG', 'TAGC')
    1.0

    """
    return Tversky().dist(src, tar, qval, alpha, beta, bias)