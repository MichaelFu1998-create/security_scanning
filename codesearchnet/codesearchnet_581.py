def find_contours(x, level=0.8, fully_connected='low', positive_orientation='low'):
    """Find iso-valued contours in a 2D array for a given level value, returns list of (n, 2)-ndarrays
    see `skimage.measure.find_contours <http://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.find_contours>`__.

    Parameters
    ------------
    x : 2D ndarray of double.
        Input data in which to find contours.
    level : float
        Value along which to find contours in the array.
    fully_connected : str
        Either `low` or `high`. Indicates whether array elements below the given level value are to be considered fully-connected (and hence elements above the value will only be face connected), or vice-versa. (See notes below for details.)
    positive_orientation : str
        Either `low` or `high`. Indicates whether the output contours will produce positively-oriented polygons around islands of low- or high-valued elements. If `low` then contours will wind counter-clockwise around elements below the iso-value. Alternately, this means that low-valued elements are always on the left of the contour.

    Returns
    --------
    list of (n,2)-ndarrays
        Each contour is an ndarray of shape (n, 2), consisting of n (row, column) coordinates along the contour.

    """
    return skimage.measure.find_contours(
        x, level, fully_connected=fully_connected, positive_orientation=positive_orientation
    )