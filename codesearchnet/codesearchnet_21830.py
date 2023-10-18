def mean(a, axis=None, dtype=None, out=None, keepdims=False):
    """
    Compute the arithmetic mean along the specified axis.

    Returns the average of the array elements.  The average is taken over
    the flattened array by default, otherwise over the specified axis.
    `float64` intermediate and return values are used for integer inputs.

    Parameters
    ----------
    a : array_like
        Array containing numbers whose mean is desired. If `a` is not an
        array, a conversion is attempted.
    axis : None or int or tuple of ints, optional
        Axis or axes along which the means are computed. The default is to
        compute the mean of the flattened array.
        If this is a tuple of ints, a mean is performed over multiple axes,
        instead of a single axis or all the axes as before.
    dtype : data-type, optional
        Type to use in computing the mean.  For integer inputs, the default
        is `float64`; for floating point inputs, it is the same as the
        input dtype.
    out : ndarray, optional
        Alternate output array in which to place the result.  The default
        is ``None``; if provided, it must have the same shape as the
        expected output, but the type will be cast if necessary.
        See `doc.ufuncs` for details.
    keepdims : bool, optional
        If this is set to True, the axes which are reduced are left
        in the result as dimensions with size one. With this option,
        the result will broadcast correctly against the original `arr`.

    Returns
    -------
    m : ndarray, see dtype parameter above

    Notes
    -----
    np.mean fails to pass the keepdims parameter to ndarray subclasses.
    That is the main reason we implement this function.
    """
    if (isinstance(a, np.ndarray) or
            isinstance(a, RemoteArray) or
            isinstance(a, DistArray)):
        return a.mean(axis=axis, dtype=dtype, out=out, keepdims=keepdims)
    else:
        return np.mean(a, axis=axis, dtype=dtype, out=out, keepdims=keepdims)