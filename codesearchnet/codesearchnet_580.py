def array_to_img(x, dim_ordering=(0, 1, 2), scale=True):
    """Converts a numpy array to PIL image object (uint8 format).

    Parameters
    ----------
    x : numpy.array
        An image with dimension of 3 and channels of 1 or 3.
    dim_ordering : tuple of 3 int
        Index of row, col and channel, default (0, 1, 2), for theano (1, 2, 0).
    scale : boolean
        If True, converts image to [0, 255] from any range of value like [-1, 2]. Default is True.

    Returns
    -------
    PIL.image
        An image.

    References
    -----------
    `PIL Image.fromarray <http://pillow.readthedocs.io/en/3.1.x/reference/Image.html?highlight=fromarray>`__

    """
    # if dim_ordering == 'default':
    #     dim_ordering = K.image_dim_ordering()
    # if dim_ordering == 'th':  # theano
    #     x = x.transpose(1, 2, 0)

    x = x.transpose(dim_ordering)

    if scale:
        x += max(-np.min(x), 0)
        x_max = np.max(x)
        if x_max != 0:
            # tl.logging.info(x_max)
            # x /= x_max
            x = x / x_max
        x *= 255

    if x.shape[2] == 3:
        # RGB
        return PIL.Image.fromarray(x.astype('uint8'), 'RGB')

    elif x.shape[2] == 1:
        # grayscale
        return PIL.Image.fromarray(x[:, :, 0].astype('uint8'), 'L')

    else:
        raise Exception('Unsupported channel number: ', x.shape[2])