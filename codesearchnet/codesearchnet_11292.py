def lmean(nums):
    r"""Return logarithmic mean.

    The logarithmic mean of an arbitrarily long series is defined by
    http://www.survo.fi/papers/logmean.pdf
    as:
    :math:`L(x_1, x_2, ..., x_n) =
    (n-1)! \sum\limits_{i=1}^n \frac{x_i}
    {\prod\limits_{\substack{j = 1\\j \ne i}}^n
    ln \frac{x_i}{x_j}}`

    Cf. https://en.wikipedia.org/wiki/Logarithmic_mean

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The logarithmic mean of nums

    Raises
    ------
    AttributeError
        No two values in the nums list may be equal

    Examples
    --------
    >>> lmean([1, 2, 3, 4])
    2.2724242417489258
    >>> lmean([1, 2])
    1.4426950408889634

    """
    if len(nums) != len(set(nums)):
        raise AttributeError('No two values in the nums list may be equal')
    rolling_sum = 0
    for i in range(len(nums)):
        rolling_prod = 1
        for j in range(len(nums)):
            if i != j:
                rolling_prod *= math.log(nums[i] / nums[j])
        rolling_sum += nums[i] / rolling_prod
    return math.factorial(len(nums) - 1) * rolling_sum