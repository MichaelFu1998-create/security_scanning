def projective_transform_by_points(
        x, src, dst, map_args=None, output_shape=None, order=1, mode='constant', cval=0.0, clip=True,
        preserve_range=False
):
    """Projective transform by given coordinates, usually 4 coordinates.

    see `scikit-image <http://scikit-image.org/docs/dev/auto_examples/applications/plot_geometric.html>`__.

    Parameters
    -----------
    x : numpy.array
        An image with dimension of [row, col, channel] (default).
    src : list or numpy
        The original coordinates, usually 4 coordinates of (width, height).
    dst : list or numpy
        The coordinates after transformation, the number of coordinates is the same with src.
    map_args : dictionary or None
        Keyword arguments passed to inverse map.
    output_shape : tuple of 2 int
        Shape of the output image generated. By default the shape of the input image is preserved. Note that, even for multi-band images, only rows and columns need to be specified.
    order : int
        The order of interpolation. The order has to be in the range 0-5:
            - 0 Nearest-neighbor
            - 1 Bi-linear (default)
            - 2 Bi-quadratic
            - 3 Bi-cubic
            - 4 Bi-quartic
            - 5 Bi-quintic
    mode : str
        One of `constant` (default), `edge`, `symmetric`, `reflect` or `wrap`.
        Points outside the boundaries of the input are filled according to the given mode. Modes match the behaviour of numpy.pad.
    cval : float
        Used in conjunction with mode `constant`, the value outside the image boundaries.
    clip : boolean
        Whether to clip the output to the range of values of the input image. This is enabled by default, since higher order interpolation may produce values outside the given input range.
    preserve_range : boolean
        Whether to keep the original range of values. Otherwise, the input image is converted according to the conventions of img_as_float.

    Returns
    -------
    numpy.array
        A processed image.

    Examples
    --------
    Assume X is an image from CIFAR-10, i.e. shape == (32, 32, 3)

    >>> src = [[0,0],[0,32],[32,0],[32,32]]     # [w, h]
    >>> dst = [[10,10],[0,32],[32,0],[32,32]]
    >>> x = tl.prepro.projective_transform_by_points(X, src, dst)

    References
    -----------
    - `scikit-image : geometric transformations <http://scikit-image.org/docs/dev/auto_examples/applications/plot_geometric.html>`__
    - `scikit-image : examples <http://scikit-image.org/docs/dev/auto_examples/index.html>`__

    """
    if map_args is None:
        map_args = {}
    # if type(src) is list:
    if isinstance(src, list):  # convert to numpy
        src = np.array(src)
    # if type(dst) is list:
    if isinstance(dst, list):
        dst = np.array(dst)
    if np.max(x) > 1:  # convert to [0, 1]
        x = x / 255

    m = transform.ProjectiveTransform()
    m.estimate(dst, src)
    warped = transform.warp(
        x, m, map_args=map_args, output_shape=output_shape, order=order, mode=mode, cval=cval, clip=clip,
        preserve_range=preserve_range
    )
    return warped