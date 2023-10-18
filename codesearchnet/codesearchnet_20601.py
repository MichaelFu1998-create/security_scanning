def get_unique_nonzeros(arr):
    """ Return a sorted list of the non-zero unique values of arr.

    Parameters
    ----------
    arr: numpy.ndarray
        The data array

    Returns
    -------
    list of items of arr.
    """
    rois = np.unique(arr)
    rois = rois[np.nonzero(rois)]
    rois.sort()

    return rois