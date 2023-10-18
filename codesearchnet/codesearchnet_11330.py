def dist_sift4(src, tar, max_offset=5, max_distance=0):
    """Return the normalized "common" Sift4 distance between two terms.

    This is a wrapper for :py:meth:`Sift4.dist`.

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
    float
        The normalized Sift4 distance

    Examples
    --------
    >>> round(dist_sift4('cat', 'hat'), 12)
    0.333333333333
    >>> dist_sift4('Niall', 'Neil')
    0.4
    >>> dist_sift4('Colin', 'Cuilen')
    0.5
    >>> dist_sift4('ATCG', 'TAGC')
    0.5

    """
    return Sift4().dist(src, tar, max_offset, max_distance)