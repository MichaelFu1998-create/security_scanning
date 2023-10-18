def sim_sift4(src, tar, max_offset=5, max_distance=0):
    """Return the normalized "common" Sift4 similarity of two terms.

    This is a wrapper for :py:meth:`Sift4.sim`.

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
        The normalized Sift4 similarity

    Examples
    --------
    >>> round(sim_sift4('cat', 'hat'), 12)
    0.666666666667
    >>> sim_sift4('Niall', 'Neil')
    0.6
    >>> sim_sift4('Colin', 'Cuilen')
    0.5
    >>> sim_sift4('ATCG', 'TAGC')
    0.5

    """
    return Sift4().sim(src, tar, max_offset, max_distance)