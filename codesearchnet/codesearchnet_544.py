def affine_zoom_matrix(zoom_range=(0.8, 1.1)):
    """Create an affine transform matrix for zooming/scaling an image's height and width.
    OpenCV format, x is width.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    zoom_range : float or tuple of 2 floats
        The zooming/scaling ratio, greater than 1 means larger.
            - float, a fixed ratio.
            - tuple of 2 floats, randomly sample a value as the ratio between these 2 values.

    Returns
    -------
    numpy.array
        An affine transform matrix.

    """

    if isinstance(zoom_range, (float, int)):
        scale = zoom_range
    elif isinstance(zoom_range, tuple):
        scale = np.random.uniform(zoom_range[0], zoom_range[1])
    else:
        raise Exception("zoom_range: float or tuple of 2 floats")

    zoom_matrix = np.array([[scale, 0, 0], \
                            [0, scale, 0], \
                            [0, 0, 1]])
    return zoom_matrix