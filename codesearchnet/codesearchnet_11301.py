def median(nums):
    """Return median.

    With numbers sorted by value, the median is the middle value (if there is
    an odd number of values) or the arithmetic mean of the two middle values
    (if there is an even number of values).

    Cf. https://en.wikipedia.org/wiki/Median

    Parameters
    ----------
    nums : list
        A series of numbers

    Returns
    -------
    int or float
        The median of nums

    Examples
    --------
    >>> median([1, 2, 3])
    2
    >>> median([1, 2, 3, 4])
    2.5
    >>> median([1, 2, 2, 4])
    2

    """
    nums = sorted(nums)
    mag = len(nums)
    if mag % 2:
        mag = int((mag - 1) / 2)
        return nums[mag]
    mag = int(mag / 2)
    med = (nums[mag - 1] + nums[mag]) / 2
    return med if not med.is_integer() else int(med)