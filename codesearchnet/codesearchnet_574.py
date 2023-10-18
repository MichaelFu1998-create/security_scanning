def featurewise_norm(x, mean=None, std=None, epsilon=1e-7):
    """Normalize every pixels by the same given mean and std, which are usually
    compute from all examples.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    mean : float
        Value for subtraction.
    std : float
        Value for division.
    epsilon : float
        A small position value for dividing standard deviation.

    Returns
    -------
    numpy.array
        A processed image.

    """
    if mean:
        x = x - mean
    if std:
        x = x / (std + epsilon)
    return x