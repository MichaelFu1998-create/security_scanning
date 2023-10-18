def imresize(x, size=None, interp='bicubic', mode=None):
    """Resize an image by given output size and method.

    Warning, this function will rescale the value to [0, 255].

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    size : list of 2 int or None
        For height and width.
    interp : str
        Interpolation method for re-sizing (`nearest`, `lanczos`, `bilinear`, `bicubic` (default) or `cubic`).
    mode : str
        The PIL image mode (`P`, `L`, etc.) to convert image before resizing.

    Returns
    -------
    numpy.array
        A processed image.

    References
    ------------
    - `scipy.misc.imresize <https://docs.scipy.org/doc/scipy/reference/generated/scipy.misc.imresize.html>`__

    """
    if size is None:
        size = [100, 100]

    if x.shape[-1] == 1:
        # greyscale
        x = scipy.misc.imresize(x[:, :, 0], size, interp=interp, mode=mode)
        return x[:, :, np.newaxis]
    else:
        # rgb, bgr, rgba
        return scipy.misc.imresize(x, size, interp=interp, mode=mode)