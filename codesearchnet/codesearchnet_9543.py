def snap_bounds(bounds=None, pyramid=None, zoom=None):
    """
    Snaps bounds to tiles boundaries of specific zoom level.

    Parameters
    ----------
    bounds : bounds to be snapped
    pyramid : TilePyramid
    zoom : int

    Returns
    -------
    Bounds(left, bottom, right, top)
    """
    if not isinstance(bounds, (tuple, list)):
        raise TypeError("bounds must be either a tuple or a list")
    if len(bounds) != 4:
        raise ValueError("bounds has to have exactly four values")
    if not isinstance(pyramid, BufferedTilePyramid):
        raise TypeError("pyramid has to be a BufferedTilePyramid")

    bounds = Bounds(*bounds)
    lb = pyramid.tile_from_xy(bounds.left, bounds.bottom, zoom, on_edge_use="rt").bounds
    rt = pyramid.tile_from_xy(bounds.right, bounds.top, zoom, on_edge_use="lb").bounds
    return Bounds(lb.left, lb.bottom, rt.right, rt.top)