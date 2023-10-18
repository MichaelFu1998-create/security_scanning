def pt2map(list_points=None, size=(100, 100), val=1):
    """Inputs a list of points, return a 2D image.

    Parameters
    --------------
    list_points : list of 2 int
        [[x, y], [x, y]..] for point coordinates.
    size : tuple of 2 int
        (w, h) for output size.
    val : float or int
        For the contour value.

    Returns
    -------
    numpy.array
        An image.

    """
    if list_points is None:
        raise Exception("list_points : list of 2 int")
    i_m = np.zeros(size)
    if len(list_points) == 0:
        return i_m
    for xx in list_points:
        for x in xx:
            # tl.logging.info(x)
            i_m[int(np.round(x[0]))][int(np.round(x[1]))] = val
    return i_m