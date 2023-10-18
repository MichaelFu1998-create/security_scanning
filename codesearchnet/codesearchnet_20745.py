def vector_to_volume(arr, mask, order='C'):
    """Transform a given vector to a volume. This is a reshape function for
    3D flattened and maybe masked vectors.

    Parameters
    ----------
    arr: np.array
        1-Dimensional array

    mask: numpy.ndarray
        Mask image. Must have 3 dimensions, bool dtype.

    Returns
    -------
    np.ndarray
    """
    if mask.dtype != np.bool:
        raise ValueError("mask must be a boolean array")

    if arr.ndim != 1:
        raise ValueError("vector must be a 1-dimensional array")

    if arr.ndim == 2 and any(v == 1 for v in arr.shape):
        log.debug('Got an array of shape {}, flattening for my purposes.'.format(arr.shape))
        arr = arr.flatten()

    volume = np.zeros(mask.shape[:3], dtype=arr.dtype, order=order)
    volume[mask] = arr
    return volume