def seiffert_mean(nums):
    r"""Return Seiffert's mean.

    Seiffert's mean of two numbers x and y is:
    :math:`\frac{x - y}{4 \cdot arctan \sqrt{\frac{x}{y}} - \pi}`

    It is defined in :cite:`Seiffert:1993`.

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    float
        Sieffert's mean of nums

    Raises
    ------
    AttributeError
        seiffert_mean supports no more than two values

    Examples
    --------
    >>> seiffert_mean([1, 2])
    1.4712939827611637
    >>> seiffert_mean([1, 0])
    0.3183098861837907
    >>> seiffert_mean([2, 4])
    2.9425879655223275
    >>> seiffert_mean([2, 1000])
    336.84053300118825

    """
    if len(nums) == 1:
        return nums[0]
    if len(nums) > 2:
        raise AttributeError('seiffert_mean supports no more than two values')
    if nums[0] + nums[1] == 0 or nums[0] - nums[1] == 0:
        return float('NaN')
    return (nums[0] - nums[1]) / (
        2 * math.asin((nums[0] - nums[1]) / (nums[0] + nums[1]))
    )