def obj_box_coord_centroid_to_upleft(coord):
    """Convert one coordinate [x_center, y_center, w, h] to [x, y, w, h].
    It is the reverse process of ``obj_box_coord_upleft_to_centroid``.

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
        raise AssertionError("coordinate should be 4 values : [x, y, w, h]")

    x_center, y_center, w, h = coord
    x = x_center - w / 2.
    y = y_center - h / 2.
    return [x, y, w, h]