def dist_hamming(src, tar, diff_lens=True):
    """Return the normalized Hamming distance between two strings.

    This is a wrapper for :py:meth:`Hamming.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    diff_lens : bool
        If True (default), this returns the Hamming distance for those
        characters that have a matching character in both strings plus the
        difference in the strings' lengths. This is equivalent to extending the
        shorter string with obligatorily non-matching characters. If False, an
        exception is raised in the case of strings of unequal lengths.

    Returns
    -------
    float
        The normalized Hamming distance

    Examples
    --------
    >>> round(dist_hamming('cat', 'hat'), 12)
    0.333333333333
    >>> dist_hamming('Niall', 'Neil')
    0.6
    >>> dist_hamming('aluminum', 'Catalan')
    1.0
    >>> dist_hamming('ATCG', 'TAGC')
    1.0

    """
    return Hamming().dist(src, tar, diff_lens)