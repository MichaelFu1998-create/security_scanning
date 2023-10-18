def sim_eudex(src, tar, weights='exponential', max_length=8):
    """Return normalized Hamming similarity between Eudex hashes of two terms.

    This is a wrapper for :py:meth:`Eudex.sim`.

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
        The normalized Eudex Hamming similarity

    Examples
    --------
    >>> round(sim_eudex('cat', 'hat'), 12)
    0.937254901961
    >>> round(sim_eudex('Niall', 'Neil'), 12)
    0.999019607843
    >>> round(sim_eudex('Colin', 'Cuilen'), 12)
    0.995098039216
    >>> round(sim_eudex('ATCG', 'TAGC'), 12)
    0.802450980392

    """
    return Eudex().sim(src, tar, weights, max_length)