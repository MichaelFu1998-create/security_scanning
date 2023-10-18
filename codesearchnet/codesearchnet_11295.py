def lehmer_mean(nums, exp=2):
    r"""Return Lehmer mean.

    The Lehmer mean is:
    :math:`\frac{\sum\limits_i{x_i^p}}{\sum\limits_i{x_i^(p-1)}}`

    Cf. https://en.wikipedia.org/wiki/Lehmer_mean

    Parameters
    ----------
    nums : list
        A series of numbers
    exp : numeric
        The exponent of the Lehmer mean

    Returns
    -------
    float
        The Lehmer mean of nums for the given exponent

    Examples
    --------
    >>> lehmer_mean([1, 2, 3, 4])
    3.0
    >>> lehmer_mean([1, 2])
    1.6666666666666667
    >>> lehmer_mean([0, 5, 1000])
    995.0497512437811

    """
    return sum(x ** exp for x in nums) / sum(x ** (exp - 1) for x in nums)