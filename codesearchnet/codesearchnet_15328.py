def _convert_coordinatelist(input_obj):
    """convert from 'list' or 'tuple' object to pgmagick.CoordinateList.

    :type input_obj: list or tuple
    """
    cdl = pgmagick.CoordinateList()
    for obj in input_obj:
        cdl.append(pgmagick.Coordinate(obj[0], obj[1]))
    return cdl