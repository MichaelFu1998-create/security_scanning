def sift4_common(src, tar, max_offset=5, max_distance=0):
    """Return the "common" Sift4 distance between two terms.

    This is a wrapper for :py:meth:`Sift4.dist_abs`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    max_offset : int
        The number of characters to search for matching letters
    max_distance : int
        The distance at which to stop and exit

    Returns
    -------
    int
        The Sift4 distance according to the common formula

    Examples
    --------
    >>> sift4_common('cat', 'hat')
    1
    >>> sift4_common('Niall', 'Neil')
    2
    >>> sift4_common('Colin', 'Cuilen')
    3
    >>> sift4_common('ATCG', 'TAGC')
    2

    """
    return Sift4().dist_abs(src, tar, max_offset, max_distance)