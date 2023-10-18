def sim_jaro_winkler(
    src,
    tar,
    qval=1,
    mode='winkler',
    long_strings=False,
    boost_threshold=0.7,
    scaling_factor=0.1,
):
    """Return the Jaro or Jaro-Winkler similarity of two strings.

    This is a wrapper for :py:meth:`JaroWinkler.sim`.

    Parameters
    ----------
    src : str
        Source string for comparison
    tar : str
        Target string for comparison
    qval : int
        The length of each q-gram (defaults to 1: character-wise matching)
    mode : str
        Indicates which variant of this distance metric to compute:

            - ``winkler`` -- computes the Jaro-Winkler distance (default) which
              increases the score for matches near the start of the word
            - ``jaro`` -- computes the Jaro distance

    long_strings : bool
        Set to True to "Increase the probability of a match when the number of
        matched characters is large. This option allows for a little more
        tolerance when the strings are large. It is not an appropriate test
        when comparing fixedlength fields such as phone and social security
        numbers." (Used in 'winkler' mode only.)
    boost_threshold : float
        A value between 0 and 1, below which the Winkler boost is not applied
        (defaults to 0.7). (Used in 'winkler' mode only.)
    scaling_factor : float
        A value between 0 and 0.25, indicating by how much to boost scores for
        matching prefixes (defaults to 0.1). (Used in 'winkler' mode only.)

    Returns
    -------
    float
        Jaro or Jaro-Winkler similarity

    Examples
    --------
    >>> round(sim_jaro_winkler('cat', 'hat'), 12)
    0.777777777778
    >>> round(sim_jaro_winkler('Niall', 'Neil'), 12)
    0.805
    >>> round(sim_jaro_winkler('aluminum', 'Catalan'), 12)
    0.60119047619
    >>> round(sim_jaro_winkler('ATCG', 'TAGC'), 12)
    0.833333333333

    >>> round(sim_jaro_winkler('cat', 'hat', mode='jaro'), 12)
    0.777777777778
    >>> round(sim_jaro_winkler('Niall', 'Neil', mode='jaro'), 12)
    0.783333333333
    >>> round(sim_jaro_winkler('aluminum', 'Catalan', mode='jaro'), 12)
    0.60119047619
    >>> round(sim_jaro_winkler('ATCG', 'TAGC', mode='jaro'), 12)
    0.833333333333

    """
    return JaroWinkler().sim(
        src, tar, qval, mode, long_strings, boost_threshold, scaling_factor
    )