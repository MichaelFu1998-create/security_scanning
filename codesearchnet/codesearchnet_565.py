def brightness(x, gamma=1, gain=1, is_random=False):
    """Change the brightness of a single image, randomly or non-randomly.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    gamma : float
        Non negative real number. Default value is 1.
            - Small than 1 means brighter.
            - If `is_random` is True, gamma in a range of (1-gamma, 1+gamma).
    gain : float
        The constant multiplier. Default value is 1.
    is_random : boolean
        If True, randomly change brightness. Default is False.

    Returns
    -------
    numpy.array
        A processed image.

    References
    -----------
    - `skimage.exposure.adjust_gamma <http://scikit-image.org/docs/dev/api/skimage.exposure.html>`__
    - `chinese blog <http://www.cnblogs.com/denny402/p/5124402.html>`__

    """
    if is_random:
        gamma = np.random.uniform(1 - gamma, 1 + gamma)
    x = exposure.adjust_gamma(x, gamma, gain)
    return x