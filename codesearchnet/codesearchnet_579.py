def drop(x, keep=0.5):
    """Randomly set some pixels to zero by a given keeping probability.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] or [row, col].
    keep : float
        The keeping probability (0, 1), the lower more values will be set to zero.

    Returns
    -------
    numpy.array
        A processed image.

    """
    if len(x.shape) == 3:
        if x.shape[-1] == 3:  # color
            img_size = x.shape
            mask = np.random.binomial(n=1, p=keep, size=x.shape[:-1])
            for i in range(3):
                x[:, :, i] = np.multiply(x[:, :, i], mask)
        elif x.shape[-1] == 1:  # greyscale image
            img_size = x.shape
            x = np.multiply(x, np.random.binomial(n=1, p=keep, size=img_size))
        else:
            raise Exception("Unsupported shape {}".format(x.shape))
    elif len(x.shape) == 2 or 1:  # greyscale matrix (image) or vector
        img_size = x.shape
        x = np.multiply(x, np.random.binomial(n=1, p=keep, size=img_size))
    else:
        raise Exception("Unsupported shape {}".format(x.shape))
    return x