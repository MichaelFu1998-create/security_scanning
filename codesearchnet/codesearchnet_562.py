def zoom(x, zoom_range=(0.9, 1.1), flags=None, border_mode='constant'):
    """Zooming/Scaling a single image that height and width are changed together.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    zoom_range : float or tuple of 2 floats
        The zooming/scaling ratio, greater than 1 means larger.
            - float, a fixed ratio.
            - tuple of 2 floats, randomly sample a value as the ratio between 2 values.
    border_mode : str
        - `constant`, pad the image with a constant value (i.e. black or 0)
        - `replicate`, the row or column at the very edge of the original is replicated to the extra border.

    Returns
    -------
    numpy.array
        A processed image.

    """
    zoom_matrix = affine_zoom_matrix(zoom_range=zoom_range)
    h, w = x.shape[0], x.shape[1]
    transform_matrix = transform_matrix_offset_center(zoom_matrix, h, w)
    x = affine_transform_cv2(x, transform_matrix, flags=flags, border_mode=border_mode)
    return x