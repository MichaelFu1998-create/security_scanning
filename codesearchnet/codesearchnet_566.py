def brightness_multi(x, gamma=1, gain=1, is_random=False):
    """Change the brightness of multiply images, randomly or non-randomly.
    Usually be used for image segmentation which x=[X, Y], X and Y should be matched.

    Parameters
    -----------
    x : list of numpyarray
        List of images with dimension of [n_images, row, col, channel] (default).
    others : args
        See ``tl.prepro.brightness``.

    Returns
    -------
    numpy.array
        A list of processed images.

    """
    if is_random:
        gamma = np.random.uniform(1 - gamma, 1 + gamma)

    results = []
    for data in x:
        results.append(exposure.adjust_gamma(data, gamma, gain))
    return np.asarray(results)