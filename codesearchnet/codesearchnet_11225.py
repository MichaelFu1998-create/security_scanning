def chebyshev(src, tar, qval=2, alphabet=None):
    r"""Return the Chebyshev distance between two strings.

    This is a wrapper for the :py:meth:`Chebyshev.dist_abs`.

    Parameters
    ----------
    src : str
        Source string (or QGrams/Counter objects) for comparison
    tar : str
        Target string (or QGrams/Counter objects) for comparison
    qval : int
        The length of each q-gram; 0 for non-q-gram version alphabet
    alphabet : collection or int
        The values or size of the alphabet

    Returns
    -------
    float
        The Chebyshev distance

    Examples
    --------
    >>> chebyshev('cat', 'hat')
    1.0
    >>> chebyshev('Niall', 'Neil')
    1.0
    >>> chebyshev('Colin', 'Cuilen')
    1.0
    >>> chebyshev('ATCG', 'TAGC')
    1.0
    >>> chebyshev('ATCG', 'TAGC', qval=1)
    0.0
    >>> chebyshev('ATCGATTCGGAATTTC', 'TAGCATAATCGCCG', qval=1)
    3.0

    """
    return Chebyshev().dist_abs(src, tar, qval, alphabet)