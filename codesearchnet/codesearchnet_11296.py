def heronian_mean(nums):
    r"""Return Heronian mean.

    The Heronian mean is:
    :math:`\frac{\sum\limits_{i, j}\sqrt{{x_i \cdot x_j}}}
    {|nums| \cdot \frac{|nums| + 1}{2}}`
    for :math:`j \ge i`

    Cf. https://en.wikipedia.org/wiki/Heronian_mean

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The Heronian mean of nums

    Examples
    --------
    >>> heronian_mean([1, 2, 3, 4])
    2.3888282852609093
    >>> heronian_mean([1, 2])
    1.4714045207910316
    >>> heronian_mean([0, 5, 1000])
    179.28511301977582

    """
    mag = len(nums)
    rolling_sum = 0
    for i in range(mag):
        for j in range(i, mag):
            if nums[i] == nums[j]:
                rolling_sum += nums[i]
            else:
                rolling_sum += (nums[i] * nums[j]) ** 0.5
    return rolling_sum * 2 / (mag * (mag + 1))