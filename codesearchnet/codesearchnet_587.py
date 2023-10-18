def obj_box_coord_rescale(coord=None, shape=None):
    """Scale down one coordinates from pixel unit to the ratio of image size i.e. in the range of [0, 1].
    It is the reverse process of ``obj_box_coord_scale_to_pixelunit``.

    Parameters
    ------------
    coords : list of 4 int or None
        One coordinates of one image e.g. [x, y, w, h].
    shape : list of 2 int or None
        For [height, width].

    Returns
    -------
    list of 4 numbers
        New bounding box.

    Examples
    ---------
    >>> coord = tl.prepro.obj_box_coord_rescale(coord=[30, 40, 50, 50], shape=[100, 100])
      [0.3, 0.4, 0.5, 0.5]

    """
    if coord is None:
        coord = []
    if shape is None:
        shape = [100, 200]

    return obj_box_coords_rescale(coords=[coord], shape=shape)[0]