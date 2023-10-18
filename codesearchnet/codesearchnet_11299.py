def ghmean(nums):
    """Return geometric-harmonic mean.

    Iterates between geometric & harmonic means until they converge to
    a single value (rounded to 12 digits).

    Cf. https://en.wikipedia.org/wiki/Geometric-harmonic_mean

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The geometric-harmonic mean of nums

    Examples
    --------
    >>> ghmean([1, 2, 3, 4])
    2.058868154613003
    >>> ghmean([1, 2])
    1.3728805006183502
    >>> ghmean([0, 5, 1000])
    0.0

    >>> ghmean([0, 0])
    0.0
    >>> ghmean([0, 0, 5])
    nan

    """
    m_g = gmean(nums)
    m_h = hmean(nums)
    if math.isnan(m_g) or math.isnan(m_h):
        return float('nan')
    while round(m_h, 12) != round(m_g, 12):
        m_g, m_h = (m_g * m_h) ** (1 / 2), (2 * m_g * m_h) / (m_g + m_h)
    return m_g