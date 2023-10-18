def dist_eudex(src, tar, weights='exponential', max_length=8):
    """Return normalized Hamming distance between Eudex hashes of two terms.

    This is a wrapper for :py:meth:`Eudex.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    weights : str, iterable, or generator function
        The weights or weights generator function
    max_length : int
        The number of characters to encode as a eudex hash

    Returns
    -------
    int
        The normalized Eudex Hamming distance

    Examples
    --------
    >>> round(dist_eudex('cat', 'hat'), 12)
    0.062745098039
    >>> round(dist_eudex('Niall', 'Neil'), 12)
    0.000980392157
    >>> round(dist_eudex('Colin', 'Cuilen'), 12)
    0.004901960784
    >>> round(dist_eudex('ATCG', 'TAGC'), 12)
    0.197549019608

    """
    return Eudex().dist(src, tar, weights, max_length)