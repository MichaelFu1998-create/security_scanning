def transform_from_local(xp, yp, cphi, sphi, mx, my):
    """ Transform from the local frame to absolute space.
    """
    x = xp * cphi - yp * sphi + mx
    y = xp * sphi + yp * cphi + my
    return (x,y)