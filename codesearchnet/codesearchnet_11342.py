def eudex_hamming(
    src, tar, weights='exponential', max_length=8, normalized=False
):
    """Calculate the Hamming distance between the Eudex hashes of two terms.

    This is a wrapper for :py:meth:`Eudex.eudex_hamming`.

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
    normalized : bool
        Normalizes to [0, 1] if True

    Returns
    -------
    int
        The Eudex Hamming distance

    Examples
    --------
    >>> eudex_hamming('cat', 'hat')
    128
    >>> eudex_hamming('Niall', 'Neil')
    2
    >>> eudex_hamming('Colin', 'Cuilen')
    10
    >>> eudex_hamming('ATCG', 'TAGC')
    403

    >>> eudex_hamming('cat', 'hat', weights='fibonacci')
    34
    >>> eudex_hamming('Niall', 'Neil', weights='fibonacci')
    2
    >>> eudex_hamming('Colin', 'Cuilen', weights='fibonacci')
    7
    >>> eudex_hamming('ATCG', 'TAGC', weights='fibonacci')
    117

    >>> eudex_hamming('cat', 'hat', weights=None)
    1
    >>> eudex_hamming('Niall', 'Neil', weights=None)
    1
    >>> eudex_hamming('Colin', 'Cuilen', weights=None)
    2
    >>> eudex_hamming('ATCG', 'TAGC', weights=None)
    9

    >>> # Using the OEIS A000142:
    >>> eudex_hamming('cat', 'hat', [1, 1, 2, 6, 24, 120, 720, 5040])
    1
    >>> eudex_hamming('Niall', 'Neil', [1, 1, 2, 6, 24, 120, 720, 5040])
    720
    >>> eudex_hamming('Colin', 'Cuilen', [1, 1, 2, 6, 24, 120, 720, 5040])
    744
    >>> eudex_hamming('ATCG', 'TAGC', [1, 1, 2, 6, 24, 120, 720, 5040])
    6243

    """
    return Eudex().dist_abs(src, tar, weights, max_length, normalized)