def rotation(
        x, rg=20, is_random=False, row_index=0, col_index=1, channel_index=2, fill_mode='nearest', cval=0., order=1
):
    """Rotate an image randomly or non-randomly.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    rg : int or float
        Degree to rotate, usually 0 ~ 180.
    is_random : boolean
        If True, randomly rotate. Default is False
    row_index col_index and channel_index : int
        Index of row, col and channel, default (0, 1, 2), for theano (1, 2, 0).
    fill_mode : str
        Method to fill missing pixel, default `nearest`, more options `constant`, `reflect` or `wrap`, see `scipy ndimage affine_transform <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.interpolation.affine_transform.html>`__
    cval : float
        Value used for points outside the boundaries of the input if mode=`constant`. Default is 0.0
    order : int
        The order of interpolation. The order has to be in the range 0-5. See ``tl.prepro.affine_transform`` and `scipy ndimage affine_transform <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.interpolation.affine_transform.html>`__

    Returns
    -------
    numpy.array
        A processed image.

    Examples
    ---------
    >>> x --> [row, col, 1]
    >>> x = tl.prepro.rotation(x, rg=40, is_random=False)
    >>> tl.vis.save_image(x, 'im.png')

    """
    if is_random:
        theta = np.pi / 180 * np.random.uniform(-rg, rg)
    else:
        theta = np.pi / 180 * rg
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])

    h, w = x.shape[row_index], x.shape[col_index]
    transform_matrix = transform_matrix_offset_center(rotation_matrix, h, w)
    x = affine_transform(x, transform_matrix, channel_index, fill_mode, cval, order)
    return x