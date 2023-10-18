def _convert_vpathlist(input_obj):
    """convert from 'list' or 'tuple' object to pgmagick.VPathList.

    :type input_obj: list or tuple
    """
    vpl = pgmagick.VPathList()
    for obj in input_obj:
        # FIXME
        obj = pgmagick.PathMovetoAbs(pgmagick.Coordinate(obj[0], obj[1]))
        vpl.append(obj)
    return vpl