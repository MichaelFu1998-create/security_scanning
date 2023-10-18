def obj_box_coord_centroid_to_upleft_butright(coord, to_int=False):
    """Convert one coordinate [x_center, y_center, w, h] to [x1, y1, x2, y2] in up-left and botton-right format.

    Parameters
    ------------
    coord : list of 4 int/float
        One coordinate.
    to_int : boolean
        Whether to convert output as integer.

    Returns
    -------
    list of 4 numbers
        New bounding box.

    Examples
    ---------
    >>> coord = obj_box_coord_centroid_to_upleft_butright([30, 40, 20, 20])
      [20, 30, 40, 50]

    """
    if len(coord) != 4:
        raise AssertionError("coordinate should be 4 values : [x, y, w, h]")

    x_center, y_center, w, h = coord
    x = x_center - w / 2.
    y = y_center - h / 2.
    x2 = x + w
    y2 = y + h
    if to_int:
        return [int(x), int(y), int(x2), int(y2)]
    else:
        return [x, y, x2, y2]