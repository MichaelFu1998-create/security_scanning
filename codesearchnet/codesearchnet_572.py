def pixel_value_scale(im, val=0.9, clip=None, is_random=False):
    """Scales each value in the pixels of the image.

    Parameters
    -----------
    im : numpy.array
        An image.
    val : float
        The scale value for changing pixel value.
            - If is_random=False, multiply this value with all pixels.
            - If is_random=True, multiply a value between [1-val, 1+val] with all pixels.
    clip : tuple of 2 numbers
        The minimum and maximum value.
    is_random : boolean
        If True, see ``val``.

    Returns
    -------
    numpy.array
        A processed image.

    Examples
    ----------
    Random

    >>> im = pixel_value_scale(im, 0.1, [0, 255], is_random=True)

    Non-random

    >>> im = pixel_value_scale(im, 0.9, [0, 255], is_random=False)

    """

    clip = clip if clip is not None else (-np.inf, np.inf)

    if is_random:
        scale = 1 + np.random.uniform(-val, val)
        im = im * scale
    else:
        im = im * val

    if len(clip) == 2:
        im = np.clip(im, clip[0], clip[1])
    else:
        raise Exception("clip : tuple of 2 numbers")

    return im