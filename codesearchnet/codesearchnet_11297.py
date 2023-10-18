def hoelder_mean(nums, exp=2):
    r"""Return Hölder (power/generalized) mean.

    The Hölder mean is defined as:
    :math:`\sqrt[p]{\frac{1}{|nums|} \cdot \sum\limits_i{x_i^p}}`
    for :math:`p \ne 0`, and the geometric mean for :math:`p = 0`

    Cf. https://en.wikipedia.org/wiki/Generalized_mean

    Parameters
    ----------
    nums : list
        A series of numbers
    exp : numeric
        The exponent of the Hölder mean

    Returns
    -------
    float
        The Hölder mean of nums for the given exponent

    Examples
    --------
    >>> hoelder_mean([1, 2, 3, 4])
    2.7386127875258306
    >>> hoelder_mean([1, 2])
    1.5811388300841898
    >>> hoelder_mean([0, 5, 1000])
    577.3574860228857

    """
    if exp == 0:
        return gmean(nums)
    return ((1 / len(nums)) * sum(i ** exp for i in nums)) ** (1 / exp)