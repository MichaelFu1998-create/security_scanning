def obj_box_coord_upleft_butright_to_centroid(coord):
    """Convert one coordinate [x1, y1, x2, y2] to [x_center, y_center, w, h].
    It is the reverse process of ``obj_box_coord_centroid_to_upleft_butright``.

    Parameters
    ------------
    coord : list of 4 int/float
        One coordinate.

    Returns
    -------
    list of 4 numbers
        New bounding box.

    """
    if len(coord) != 4:
        raise AssertionError("coordinate should be 4 values : [x1, y1, x2, y2]")
    x1, y1, x2, y2 = coord
    w = x2 - x1
    h = y2 - y1
    x_c = x1 + w / 2.
    y_c = y1 + h / 2.
    return [x_c, y_c, w, h]