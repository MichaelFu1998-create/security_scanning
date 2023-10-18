def imean(nums):
    r"""Return identric (exponential) mean.

    The identric mean of two numbers x and y is:
    x if x = y
    otherwise :math:`\frac{1}{e} \sqrt[x-y]{\frac{x^x}{y^y}}`

    Cf. https://en.wikipedia.org/wiki/Identric_mean

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        The identric mean of nums

    Raises
    ------
    AttributeError
        imean supports no more than two values

    Examples
    --------
    >>> imean([1, 2])
    1.4715177646857693
    >>> imean([1, 0])
    nan
    >>> imean([2, 4])
    2.9430355293715387

    """
    if len(nums) == 1:
        return nums[0]
    if len(nums) > 2:
        raise AttributeError('imean supports no more than two values')
    if nums[0] <= 0 or nums[1] <= 0:
        return float('NaN')
    elif nums[0] == nums[1]:
        return nums[0]
    return (1 / math.e) * (nums[0] ** nums[0] / nums[1] ** nums[1]) ** (
        1 / (nums[0] - nums[1])
    )