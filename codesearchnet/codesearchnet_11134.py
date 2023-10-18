def sim_tversky(src, tar, qval=2, alpha=1, beta=1, bias=None):
    """Return the Tversky index of two strings.

    This is a wrapper for :py:meth:`Tversky.sim`.

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
        Tversky similarity

    Examples
    --------
    >>> sim_tversky('cat', 'hat')
    0.3333333333333333
    >>> sim_tversky('Niall', 'Neil')
    0.2222222222222222
    >>> sim_tversky('aluminum', 'Catalan')
    0.0625
    >>> sim_tversky('ATCG', 'TAGC')
    0.0

    """
    return Tversky().sim(src, tar, qval, alpha, beta, bias)