def var(nums, mean_func=amean, ddof=0):
    r"""Calculate the variance.

    The variance (:math:`\sigma^2`) of a series of numbers (:math:`x_i`) with
    mean :math:`\mu` and population :math:`N` is:

    :math:`\sigma^2 = \frac{1}{N}\sum_{i=1}^{N}(x_i-\mu)^2`.

    Cf. https://en.wikipedia.org/wiki/Variance

    Parameters
    ----------
    nums : list
        A series of numbers
    mean_func : function
        A mean function (amean by default)
    ddof : int
        The degrees of freedom (0 by default)

    Returns
    -------
    float
        The variance of the values in the series

    Examples
    --------
    >>> var([1, 1, 1, 1])
    0.0
    >>> var([1, 2, 3, 4])
    1.25
    >>> round(var([1, 2, 3, 4], ddof=1), 12)
    1.666666666667

    """
    x_bar = mean_func(nums)
    return sum((x - x_bar) ** 2 for x in nums) / (len(nums) - ddof)