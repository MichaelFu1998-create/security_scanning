def respective_zoom(x, h_range=(0.9, 1.1), w_range=(0.9, 1.1), flags=None, border_mode='constant'):
    """Zooming/Scaling a single image that height and width are changed independently.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    h_range : float or tuple of 2 floats
        The zooming/scaling ratio of height, greater than 1 means larger.
            - float, a fixed ratio.
            - tuple of 2 floats, randomly sample a value as the ratio between 2 values.
    w_range : float or tuple of 2 floats
        The zooming/scaling ratio of width, greater than 1 means larger.
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
    zoom_matrix = affine_respective_zoom_matrix(h_range=h_range, w_range=w_range)
    h, w = x.shape[0], x.shape[1]
    transform_matrix = transform_matrix_offset_center(zoom_matrix, h, w)
    x = affine_transform_cv2(
        x, transform_matrix, flags=flags, border_mode=border_mode
    )  #affine_transform(x, transform_matrix, channel_index, fill_mode, cval, order)
    return x