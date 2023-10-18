def affine_respective_zoom_matrix(w_range=0.8, h_range=1.1):
    """Get affine transform matrix for zooming/scaling that height and width are changed independently.
    OpenCV format, x is width.

    Parameters
    -----------
    w_range : float or tuple of 2 floats
        The zooming/scaling ratio of width, greater than 1 means larger.
            - float, a fixed ratio.
            - tuple of 2 floats, randomly sample a value as the ratio between 2 values.
    h_range : float or tuple of 2 floats
        The zooming/scaling ratio of height, greater than 1 means larger.
            - float, a fixed ratio.
            - tuple of 2 floats, randomly sample a value as the ratio between 2 values.

    Returns
    -------
    numpy.array
        An affine transform matrix.

    """

    if isinstance(h_range, (float, int)):
        zy = h_range
    elif isinstance(h_range, tuple):
        zy = np.random.uniform(h_range[0], h_range[1])
    else:
        raise Exception("h_range: float or tuple of 2 floats")

    if isinstance(w_range, (float, int)):
        zx = w_range
    elif isinstance(w_range, tuple):
        zx = np.random.uniform(w_range[0], w_range[1])
    else:
        raise Exception("w_range: float or tuple of 2 floats")

    zoom_matrix = np.array([[zx, 0, 0], \
                            [0, zy, 0], \
                            [0, 0, 1]])
    return zoom_matrix