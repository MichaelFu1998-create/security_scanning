def hmean(nums):
    r"""Return harmonic mean.

    The harmonic mean is defined as:
    :math:`\frac{|nums|}{\sum\limits_{i}\frac{1}{nums_i}}`

    Following the behavior of Wolfram|Alpha:
    - If one of the values in nums is 0, return 0.
    - If more than one value in nums is 0, return NaN.

    Cf. https://en.wikipedia.org/wiki/Harmonic_mean

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The harmonic mean of nums

    Raises
    ------
    AttributeError
        hmean requires at least one value

    Examples
    --------
    >>> hmean([1, 2, 3, 4])
    1.9200000000000004
    >>> hmean([1, 2])
    1.3333333333333333
    >>> hmean([0, 5, 1000])
    0

    """
    if len(nums) < 1:
        raise AttributeError('hmean requires at least one value')
    elif len(nums) == 1:
        return nums[0]
    else:
        for i in range(1, len(nums)):
            if nums[0] != nums[i]:
                break
        else:
            return nums[0]

    if 0 in nums:
        if nums.count(0) > 1:
            return float('nan')
        return 0
    return len(nums) / sum(1 / i for i in nums)