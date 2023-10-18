def samplewise_norm(
        x, rescale=None, samplewise_center=False, samplewise_std_normalization=False, channel_index=2, epsilon=1e-7
):
    """Normalize an image by rescale, samplewise centering and samplewise centering in order.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    rescale : float
        Rescaling factor. If None or 0, no rescaling is applied, otherwise we multiply the data by the value provided (before applying any other transformation)
    samplewise_center : boolean
        If True, set each sample mean to 0.
    samplewise_std_normalization : boolean
        If True, divide each input by its std.
    epsilon : float
        A small position value for dividing standard deviation.

    Returns
    -------
    numpy.array
        A processed image.

    Examples
    --------
    >>> x = samplewise_norm(x, samplewise_center=True, samplewise_std_normalization=True)
    >>> print(x.shape, np.mean(x), np.std(x))
    (160, 176, 1), 0.0, 1.0

    Notes
    ------
    When samplewise_center and samplewise_std_normalization are True.
    - For greyscale image, every pixels are subtracted and divided by the mean and std of whole image.
    - For RGB image, every pixels are subtracted and divided by the mean and std of this pixel i.e. the mean and std of a pixel is 0 and 1.

    """
    if rescale:
        x *= rescale

    if x.shape[channel_index] == 1:
        # greyscale
        if samplewise_center:
            x = x - np.mean(x)
        if samplewise_std_normalization:
            x = x / np.std(x)
        return x
    elif x.shape[channel_index] == 3:
        # rgb
        if samplewise_center:
            x = x - np.mean(x, axis=channel_index, keepdims=True)
        if samplewise_std_normalization:
            x = x / (np.std(x, axis=channel_index, keepdims=True) + epsilon)
        return x
    else:
        raise Exception("Unsupported channels %d" % x.shape[channel_index])