def obj_box_imresize(im, coords=None, size=None, interp='bicubic', mode=None, is_rescale=False):
    """Resize an image, and compute the new bounding box coordinates.

    Parameters
    -------------
    im : numpy.array
        An image with dimension of [row, col, channel] (default).
    coords : list of list of 4 int/float or None
        Coordinates [[x, y, w, h], [x, y, w, h], ...]
    size interp and mode : args
        See ``tl.prepro.imresize``.
    is_rescale : boolean
        Set to True, if the input coordinates are rescaled to [0, 1], then return the original coordinates. Default is False.

    Returns
    -------
    numpy.array
        A processed image
    list of list of 4 numbers
        A list of new bounding boxes.

    Examples
    --------
    >>> im = np.zeros([80, 100, 3])    # as an image with shape width=100, height=80
    >>> _, coords = obj_box_imresize(im, coords=[[20, 40, 30, 30], [10, 20, 20, 20]], size=[160, 200], is_rescale=False)
    >>> print(coords)
      [[40, 80, 60, 60], [20, 40, 40, 40]]
    >>> _, coords = obj_box_imresize(im, coords=[[20, 40, 30, 30]], size=[40, 100], is_rescale=False)
    >>> print(coords)
      [[20, 20, 30, 15]]
    >>> _, coords = obj_box_imresize(im, coords=[[20, 40, 30, 30]], size=[60, 150], is_rescale=False)
    >>> print(coords)
      [[30, 30, 45, 22]]
    >>> im2, coords = obj_box_imresize(im, coords=[[0.2, 0.4, 0.3, 0.3]], size=[160, 200], is_rescale=True)
    >>> print(coords, im2.shape)
      [[0.2, 0.4, 0.3, 0.3]] (160, 200, 3)

    """
    if coords is None:
        coords = []
    if size is None:
        size = [100, 100]

    imh, imw = im.shape[0:2]
    imh = imh * 1.0  # * 1.0 for python2 : force division to be float point
    imw = imw * 1.0
    im = imresize(im, size=size, interp=interp, mode=mode)

    if is_rescale is False:
        coords_new = list()

        for coord in coords:

            if len(coord) != 4:
                raise AssertionError("coordinate should be 4 values : [x, y, w, h]")

            # x' = x * (imw'/imw)
            x = int(coord[0] * (size[1] / imw))
            # y' = y * (imh'/imh)
            # tl.logging.info('>>', coord[1], size[0], imh)
            y = int(coord[1] * (size[0] / imh))
            # w' = w * (imw'/imw)
            w = int(coord[2] * (size[1] / imw))
            # h' = h * (imh'/imh)
            h = int(coord[3] * (size[0] / imh))
            coords_new.append([x, y, w, h])
        return im, coords_new
    else:
        return im, coords