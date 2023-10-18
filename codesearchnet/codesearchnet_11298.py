def agmean(nums):
    """Return arithmetic-geometric mean.

    Iterates between arithmetic & geometric means until they converge to
    a single value (rounded to 12 digits).

    Cf. https://en.wikipedia.org/wiki/Arithmetic-geometric_mean

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The arithmetic-geometric mean of nums

    Examples
    --------
    >>> agmean([1, 2, 3, 4])
    2.3545004777751077
    >>> agmean([1, 2])
    1.4567910310469068
    >>> agmean([0, 5, 1000])
    2.9753977059954195e-13

    """
    m_a = amean(nums)
    m_g = gmean(nums)
    if math.isnan(m_a) or math.isnan(m_g):
        return float('nan')
    while round(m_a, 12) != round(m_g, 12):
        m_a, m_g = (m_a + m_g) / 2, (m_a * m_g) ** (1 / 2)
    return m_a