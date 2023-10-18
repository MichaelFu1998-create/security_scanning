def shear2(
        x, shear=(0.1, 0.1), is_random=False, row_index=0, col_index=1, channel_index=2, fill_mode='nearest', cval=0.,
        order=1
):
    """Shear an image randomly or non-randomly.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    shear : tuple of two floats
        Percentage of shear for height and width direction (0, 1).
    is_random : boolean
        If True, randomly shear. Default is False.
    row_index col_index and channel_index : int
        Index of row, col and channel, default (0, 1, 2), for theano (1, 2, 0).
    fill_mode : str
        Method to fill missing pixel, default `nearest`, more options `constant`, `reflect` or `wrap`, see `scipy ndimage affine_transform <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.interpolation.affine_transform.html>`__
    cval : float
        Value used for points outside the boundaries of the input if mode='constant'. Default is 0.0.
    order : int
        The order of interpolation. The order has to be in the range 0-5. See ``tl.prepro.affine_transform`` and `scipy ndimage affine_transform <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.interpolation.affine_transform.html>`__

    Returns
    -------
    numpy.array
        A processed image.

    References
    -----------
    - `Affine transformation <https://uk.mathworks.com/discovery/affine-transformation.html>`__

    """
    if len(shear) != 2:
        raise AssertionError(
            "shear should be tuple of 2 floats, or you want to use tl.prepro.shear rather than tl.prepro.shear2 ?"
        )
    if isinstance(shear, tuple):
        shear = list(shear)
    if is_random:
        shear[0] = np.random.uniform(-shear[0], shear[0])
        shear[1] = np.random.uniform(-shear[1], shear[1])

    shear_matrix = np.array([[1, shear[0], 0], \
                            [shear[1], 1, 0], \
                            [0, 0, 1]])

    h, w = x.shape[row_index], x.shape[col_index]
    transform_matrix = transform_matrix_offset_center(shear_matrix, h, w)
    x = affine_transform(x, transform_matrix, channel_index, fill_mode, cval, order)
    return x