def levenshtein(src, tar, mode='lev', cost=(1, 1, 1, 1)):
    """Return the Levenshtein distance between two strings.

    This is a wrapper of :py:meth:`Levenshtein.dist_abs`.

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
    int (may return a float if cost has float values)
        The Levenshtein distance between src & tar

    Examples
    --------
    >>> levenshtein('cat', 'hat')
    1
    >>> levenshtein('Niall', 'Neil')
    3
    >>> levenshtein('aluminum', 'Catalan')
    7
    >>> levenshtein('ATCG', 'TAGC')
    3

    >>> levenshtein('ATCG', 'TAGC', mode='osa')
    2
    >>> levenshtein('ACTG', 'TAGC', mode='osa')
    4

    """
    return Levenshtein().dist_abs(src, tar, mode, cost)