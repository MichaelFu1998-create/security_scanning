def aghmean(nums):
    """Return arithmetic-geometric-harmonic mean.

    Iterates over arithmetic, geometric, & harmonic means until they
    converge to a single value (rounded to 12 digits), following the
    method described in :cite:`Raissouli:2009`.

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The arithmetic-geometric-harmonic mean of nums

    Examples
    --------
    >>> aghmean([1, 2, 3, 4])
    2.198327159900212
    >>> aghmean([1, 2])
    1.4142135623731884
    >>> aghmean([0, 5, 1000])
    335.0

    """
    m_a = amean(nums)
    m_g = gmean(nums)
    m_h = hmean(nums)
    if math.isnan(m_a) or math.isnan(m_g) or math.isnan(m_h):
        return float('nan')
    while round(m_a, 12) != round(m_g, 12) and round(m_g, 12) != round(
        m_h, 12
    ):
        m_a, m_g, m_h = (
            (m_a + m_g + m_h) / 3,
            (m_a * m_g * m_h) ** (1 / 3),
            3 / (1 / m_a + 1 / m_g + 1 / m_h),
        )
    return m_a