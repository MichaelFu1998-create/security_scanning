def sim_hamming(src, tar, diff_lens=True):
    """Return the normalized Hamming similarity of two strings.

    This is a wrapper for :py:meth:`Hamming.sim`.

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
        The normalized Hamming similarity

    Examples
    --------
    >>> round(sim_hamming('cat', 'hat'), 12)
    0.666666666667
    >>> sim_hamming('Niall', 'Neil')
    0.4
    >>> sim_hamming('aluminum', 'Catalan')
    0.0
    >>> sim_hamming('ATCG', 'TAGC')
    0.0

    """
    return Hamming().sim(src, tar, diff_lens)