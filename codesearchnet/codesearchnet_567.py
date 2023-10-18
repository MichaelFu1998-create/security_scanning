def illumination(x, gamma=1., contrast=1., saturation=1., is_random=False):
    """Perform illumination augmentation for a single image, randomly or non-randomly.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    gamma : float
        Change brightness (the same with ``tl.prepro.brightness``)
            - if is_random=False, one float number, small than one means brighter, greater than one means darker.
            - if is_random=True, tuple of two float numbers, (min, max).
    contrast : float
        Change contrast.
            - if is_random=False, one float number, small than one means blur.
            - if is_random=True, tuple of two float numbers, (min, max).
    saturation : float
        Change saturation.
            - if is_random=False, one float number, small than one means unsaturation.
            - if is_random=True, tuple of two float numbers, (min, max).
    is_random : boolean
        If True, randomly change illumination. Default is False.

    Returns
    -------
    numpy.array
        A processed image.

    Examples
    ---------
    Random

    >>> x = tl.prepro.illumination(x, gamma=(0.5, 5.0), contrast=(0.3, 1.0), saturation=(0.7, 1.0), is_random=True)

    Non-random

    >>> x = tl.prepro.illumination(x, 0.5, 0.6, 0.8, is_random=False)

    """
    if is_random:
        if not (len(gamma) == len(contrast) == len(saturation) == 2):
            raise AssertionError("if is_random = True, the arguments are (min, max)")

        ## random change brightness  # small --> brighter
        illum_settings = np.random.randint(0, 3)  # 0-brighter, 1-darker, 2 keep normal

        if illum_settings == 0:  # brighter
            gamma = np.random.uniform(gamma[0], 1.0)  # (.5, 1.0)
        elif illum_settings == 1:  # darker
            gamma = np.random.uniform(1.0, gamma[1])  # (1.0, 5.0)
        else:
            gamma = 1
        im_ = brightness(x, gamma=gamma, gain=1, is_random=False)

        # tl.logging.info("using contrast and saturation")
        image = PIL.Image.fromarray(im_)  # array -> PIL
        contrast_adjust = PIL.ImageEnhance.Contrast(image)
        image = contrast_adjust.enhance(np.random.uniform(contrast[0], contrast[1]))  #0.3,0.9))

        saturation_adjust = PIL.ImageEnhance.Color(image)
        image = saturation_adjust.enhance(np.random.uniform(saturation[0], saturation[1]))  # (0.7,1.0))
        im_ = np.array(image)  # PIL -> array
    else:
        im_ = brightness(x, gamma=gamma, gain=1, is_random=False)
        image = PIL.Image.fromarray(im_)  # array -> PIL
        contrast_adjust = PIL.ImageEnhance.Contrast(image)
        image = contrast_adjust.enhance(contrast)

        saturation_adjust = PIL.ImageEnhance.Color(image)
        image = saturation_adjust.enhance(saturation)
        im_ = np.array(image)  # PIL -> array
    return np.asarray(im_)