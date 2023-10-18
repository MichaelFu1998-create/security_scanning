def onehot_like(a, index, value=1):
    """Creates an array like a, with all values
    set to 0 except one.

    Parameters
    ----------
    a : array_like
        The returned one-hot array will have the same shape
        and dtype as this array
    index : int
        The index that should be set to `value`
    value : single value compatible with a.dtype
        The value to set at the given index

    Returns
    -------
    `numpy.ndarray`
        One-hot array with the given value at the given
        location and zeros everywhere else.

    """

    x = np.zeros_like(a)
    x[index] = value
    return x