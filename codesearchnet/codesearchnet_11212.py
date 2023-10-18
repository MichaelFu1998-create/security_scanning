def hamming(src, tar, diff_lens=True):
    """Return the Hamming distance between two strings.

    This is a wrapper for :py:meth:`Hamming.dist_abs`.

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
    int
        The Hamming distance between src & tar

    Examples
    --------
    >>> hamming('cat', 'hat')
    1
    >>> hamming('Niall', 'Neil')
    3
    >>> hamming('aluminum', 'Catalan')
    8
    >>> hamming('ATCG', 'TAGC')
    4

    """
    return Hamming().dist_abs(src, tar, diff_lens)