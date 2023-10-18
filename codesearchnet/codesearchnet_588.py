def obj_box_coord_scale_to_pixelunit(coord, shape=None):
    """Convert one coordinate [x, y, w (or x2), h (or y2)] in ratio format to image coordinate format.
    It is the reverse process of ``obj_box_coord_rescale``.

    Parameters
    -----------
    coord : list of 4 float
        One coordinate of one image [x, y, w (or x2), h (or y2)] in ratio format, i.e value range [0~1].
    shape : tuple of 2 or None
        For [height, width].

    Returns
    -------
    list of 4 numbers
        New bounding box.

    Examples
    ---------
    >>> x, y, x2, y2 = tl.prepro.obj_box_coord_scale_to_pixelunit([0.2, 0.3, 0.5, 0.7], shape=(100, 200, 3))
      [40, 30, 100, 70]

    """
    if shape is None:
        shape = [100, 100]

    imh, imw = shape[0:2]
    x = int(coord[0] * imw)
    x2 = int(coord[2] * imw)
    y = int(coord[1] * imh)
    y2 = int(coord[3] * imh)
    return [x, y, x2, y2]