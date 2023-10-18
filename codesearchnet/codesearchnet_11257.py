def dist_levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the normalized Levenshtein distance between two strings.

    This is a wrapper of :py:meth:`Levenshtein.dist`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    mode : str
        Specifies a mode for computing the Levenshtein distance:

            - ``lev`` (default) computes the ordinary Levenshtein distance, in
              which edits may include inserts, deletes, and substitutions
            - ``osa`` computes the Optimal String Alignment distance, in which
              edits may include inserts, deletes, substitutions, and
              transpositions but substrings may only be edited once

    cost : tuple
        A 4-tuple representing the cost of the four possible edits: inserts,
        deletes, substitutions, and transpositions, respectively (by default:
        (1, 1, 1, 1))

    Returns
    -------
    float
        The Levenshtein distance between src & tar

    Examples
    --------
    >>> round(dist_levenshtein('cat', 'hat'), 12)
    0.333333333333
    >>> round(dist_levenshtein('Niall', 'Neil'), 12)
    0.6
    >>> dist_levenshtein('aluminum', 'Catalan')
    0.875
    >>> dist_levenshtein('ATCG', 'TAGC')
    0.75

    """
    return Levenshtein().dist(src, tar, mode, cost)