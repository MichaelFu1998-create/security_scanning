def NonUniformImage_axes(img):
    """
    Returns axes *x, y* for a given image *img* to be used with :func:`scisalt.matplotlib.NonUniformImage`.

    Returns
    -------
    x, y : float, float
    """
    xmin = 0
    xmax = img.shape[1]-1
    ymin = 0
    ymax = img.shape[0]-1
    x = _np.linspace(xmin, xmax, img.shape[1])
    y = _np.linspace(ymin, ymax, img.shape[0])
    return x, y