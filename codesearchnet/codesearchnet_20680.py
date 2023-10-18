def is_valid_coordinate(img, i, j, k):
    """Return True if the given (i, j, k) voxel grid coordinate values are within the img boundaries.

    Parameters
    ----------
    @param img:
    @param i:
    @param j:
    @param k:

    Returns
    -------
    bool
    """
    imgx, imgy, imgz = get_shape(img)
    return (i >= 0 and i < imgx) and \
           (j >= 0 and j < imgy) and \
           (k >= 0 and k < imgz)