def binarize(x, values, threshold=None, included_in='upper'):
    """Binarizes the values of x.

    Parameters
    ----------
    values : tuple of two floats
        The lower and upper value to which the inputs are mapped.
    threshold : float
        The threshold; defaults to (values[0] + values[1]) / 2 if None.
    included_in : str
        Whether the threshold value itself belongs to the lower or
        upper interval.

    """
    lower, upper = values

    if threshold is None:
        threshold = (lower + upper) / 2.

    x = x.copy()
    if included_in == 'lower':
        x[x <= threshold] = lower
        x[x > threshold] = upper
    elif included_in == 'upper':
        x[x < threshold] = lower
        x[x >= threshold] = upper
    else:
        raise ValueError('included_in must be "lower" or "upper"')
    return x