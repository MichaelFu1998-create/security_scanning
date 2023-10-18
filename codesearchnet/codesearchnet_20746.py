def matrix_to_4dvolume(arr, mask, order='C'):
    """Transform a given vector to a volume. This is a reshape function for
    4D flattened masked matrices where the second dimension of the matrix
    corresponds to the original 4th dimension.

    Parameters
    ----------
    arr: numpy.array
        2D numpy.array

    mask: numpy.ndarray
        Mask image. Must have 3 dimensions, bool dtype.

    dtype: return type
        If None, will get the type from vector

    Returns
    -------
    data: numpy.ndarray
        Unmasked data.
        Shape: (mask.shape[0], mask.shape[1], mask.shape[2], X.shape[1])
    """
    if mask.dtype != np.bool:
        raise ValueError("mask must be a boolean array")

    if arr.ndim != 2:
        raise ValueError("X must be a 2-dimensional array")

    if mask.sum() != arr.shape[0]:
        # raise an error if the shape of arr is not what expected
        raise ValueError('Expected arr of shape ({}, samples). Got {}.'.format(mask.sum(), arr.shape))

    data = np.zeros(mask.shape + (arr.shape[1],), dtype=arr.dtype,
                    order=order)
    data[mask, :] = arr
    return data