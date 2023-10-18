def swirl(
        x, center=None, strength=1, radius=100, rotation=0, output_shape=None, order=1, mode='constant', cval=0,
        clip=True, preserve_range=False, is_random=False
):
    """Swirl an image randomly or non-randomly, see `scikit-image swirl API <http://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.swirl>`__
    and `example <http://scikit-image.org/docs/dev/auto_examples/plot_swirl.html>`__.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    center : tuple or 2 int or None
        Center coordinate of transformation (optional).
    strength : float
        The amount of swirling applied.
    radius : float
        The extent of the swirl in pixels. The effect dies out rapidly beyond radius.
    rotation : float
        Additional rotation applied to the image, usually [0, 360], relates to center.
    output_shape : tuple of 2 int or None
        Shape of the output image generated (height, width). By default the shape of the input image is preserved.
    order : int, optional
        The order of the spline interpolation, default is 1. The order has to be in the range 0-5. See skimage.transform.warp for detail.
    mode : str
        One of `constant` (default), `edge`, `symmetric` `reflect` and `wrap`.
        Points outside the boundaries of the input are filled according to the given mode, with `constant` used as the default. Modes match the behaviour of numpy.pad.
    cval : float
        Used in conjunction with mode `constant`, the value outside the image boundaries.
    clip : boolean
        Whether to clip the output to the range of values of the input image. This is enabled by default, since higher order interpolation may produce values outside the given input range.
    preserve_range : boolean
        Whether to keep the original range of values. Otherwise, the input image is converted according to the conventions of img_as_float.
    is_random : boolean,
        If True, random swirl. Default is False.
            - random center = [(0 ~ x.shape[0]), (0 ~ x.shape[1])]
            - random strength = [0, strength]
            - random radius = [1e-10, radius]
            - random rotation = [-rotation, rotation]

    Returns
    -------
    numpy.array
        A processed image.

    Examples
    ---------
    >>> x --> [row, col, 1] greyscale
    >>> x = tl.prepro.swirl(x, strength=4, radius=100)

    """
    if radius == 0:
        raise AssertionError("Invalid radius value")

    rotation = np.pi / 180 * rotation
    if is_random:
        center_h = int(np.random.uniform(0, x.shape[0]))
        center_w = int(np.random.uniform(0, x.shape[1]))
        center = (center_h, center_w)
        strength = np.random.uniform(0, strength)
        radius = np.random.uniform(1e-10, radius)
        rotation = np.random.uniform(-rotation, rotation)

    max_v = np.max(x)
    if max_v > 1:  # Note: the input of this fn should be [-1, 1], rescale is required.
        x = x / max_v
    swirled = skimage.transform.swirl(
        x, center=center, strength=strength, radius=radius, rotation=rotation, output_shape=output_shape, order=order,
        mode=mode, cval=cval, clip=clip, preserve_range=preserve_range
    )
    if max_v > 1:
        swirled = swirled * max_v
    return swirled