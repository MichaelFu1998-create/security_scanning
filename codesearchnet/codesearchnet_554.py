def flip_axis(x, axis=1, is_random=False):
    """Flip the axis of an image, such as flip left and right, up and down, randomly or non-randomly,

    Parameters
    ----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    axis : int
        Which axis to flip.
            - 0, flip up and down
            - 1, flip left and right
            - 2, flip channel
    is_random : boolean
        If True, randomly flip. Default is False.

    Returns
    -------
    numpy.array
        A processed image.

    """
    if is_random:
        factor = np.random.uniform(-1, 1)
        if factor > 0:
            x = np.asarray(x).swapaxes(axis, 0)
            x = x[::-1, ...]
            x = x.swapaxes(0, axis)
            return x
        else:
            return x
    else:
        x = np.asarray(x).swapaxes(axis, 0)
        x = x[::-1, ...]
        x = x.swapaxes(0, axis)
        return x