def count_tiles(geometry, pyramid, minzoom, maxzoom, init_zoom=0):
    """
    Count number of tiles intersecting with geometry.

    Parameters
    ----------
    geometry : shapely geometry
    pyramid : TilePyramid
    minzoom : int
    maxzoom : int
    init_zoom : int

    Returns
    -------
    number of tiles
    """
    if not 0 <= init_zoom <= minzoom <= maxzoom:
        raise ValueError("invalid zoom levels given")
    # tile buffers are not being taken into account
    unbuffered_pyramid = TilePyramid(
        pyramid.grid, tile_size=pyramid.tile_size,
        metatiling=pyramid.metatiling
    )
    # make sure no rounding errors occur
    geometry = geometry.buffer(-0.000000001)
    return _count_tiles(
        [
            unbuffered_pyramid.tile(*tile_id)
            for tile_id in product(
                [init_zoom],
                range(pyramid.matrix_height(init_zoom)),
                range(pyramid.matrix_width(init_zoom))
            )
        ], geometry, minzoom, maxzoom
    )