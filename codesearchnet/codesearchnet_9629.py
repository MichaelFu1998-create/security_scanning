def create_mosaic(tiles, nodata=0):
    """
    Create a mosaic from tiles. Tiles must be connected (also possible over Antimeridian),
    otherwise strange things can happen!

    Parameters
    ----------
    tiles : iterable
        an iterable containing tuples of a BufferedTile and an array
    nodata : integer or float
        raster nodata value to initialize the mosaic with (default: 0)

    Returns
    -------
    mosaic : ReferencedRaster
    """
    if isinstance(tiles, GeneratorType):
        tiles = list(tiles)
    elif not isinstance(tiles, list):
        raise TypeError("tiles must be either a list or generator")
    if not all([isinstance(pair, tuple) for pair in tiles]):
        raise TypeError("tiles items must be tuples")
    if not all([
        all([isinstance(tile, BufferedTile), isinstance(data, np.ndarray)])
        for tile, data in tiles
    ]):
        raise TypeError("tuples must be pairs of BufferedTile and array")
    if len(tiles) == 0:
        raise ValueError("tiles list is empty")

    logger.debug("create mosaic from %s tile(s)", len(tiles))
    # quick return if there is just one tile
    if len(tiles) == 1:
        tile, data = tiles[0]
        return ReferencedRaster(
            data=data,
            affine=tile.affine,
            bounds=tile.bounds,
            crs=tile.crs
        )

    # assert all tiles have same properties
    pyramid, resolution, dtype = _get_tiles_properties(tiles)
    # just handle antimeridian on global pyramid types
    shift = _shift_required(tiles)
    # determine mosaic shape and reference
    m_left, m_bottom, m_right, m_top = None, None, None, None
    for tile, data in tiles:
        num_bands = data.shape[0] if data.ndim > 2 else 1
        left, bottom, right, top = tile.bounds
        if shift:
            # shift by half of the grid width
            left += pyramid.x_size / 2
            right += pyramid.x_size / 2
            # if tile is now shifted outside pyramid bounds, move within
            if right > pyramid.right:
                right -= pyramid.x_size
                left -= pyramid.x_size
        m_left = min([left, m_left]) if m_left is not None else left
        m_bottom = min([bottom, m_bottom]) if m_bottom is not None else bottom
        m_right = max([right, m_right]) if m_right is not None else right
        m_top = max([top, m_top]) if m_top is not None else top
    height = int(round((m_top - m_bottom) / resolution))
    width = int(round((m_right - m_left) / resolution))
    # initialize empty mosaic
    mosaic = ma.MaskedArray(
        data=np.full((num_bands, height, width), dtype=dtype, fill_value=nodata),
        mask=np.ones((num_bands, height, width))
    )
    # create Affine
    affine = Affine(resolution, 0, m_left, 0, -resolution, m_top)
    # fill mosaic array with tile data
    for tile, data in tiles:
        data = prepare_array(data, nodata=nodata, dtype=dtype)
        t_left, t_bottom, t_right, t_top = tile.bounds
        if shift:
            t_left += pyramid.x_size / 2
            t_right += pyramid.x_size / 2
            # if tile is now shifted outside pyramid bounds, move within
            if t_right > pyramid.right:
                t_right -= pyramid.x_size
                t_left -= pyramid.x_size
        minrow, maxrow, mincol, maxcol = bounds_to_ranges(
            out_bounds=(t_left, t_bottom, t_right, t_top),
            in_affine=affine,
            in_shape=(height, width)
        )
        mosaic[:, minrow:maxrow, mincol:maxcol] = data
        mosaic.mask[:, minrow:maxrow, mincol:maxcol] = data.mask
    if shift:
        # shift back output mosaic
        affine = Affine(resolution, 0, m_left - pyramid.x_size / 2, 0, -resolution, m_top)
    return ReferencedRaster(
        data=mosaic,
        affine=affine,
        bounds=Bounds(m_left, m_bottom, m_right, m_top),
        crs=tile.crs
    )