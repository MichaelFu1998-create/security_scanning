def tile_to_zoom_level(tile, dst_pyramid=None, matching_method="gdal", precision=8):
    """
    Determine the best zoom level in target TilePyramid from given Tile.


    Parameters
    ----------
    tile : BufferedTile
    dst_pyramid : BufferedTilePyramid
    matching_method : str ('gdal' or 'min')
        gdal: Uses GDAL's standard method. Here, the target resolution is calculated by
            averaging the extent's pixel sizes over both x and y axes. This approach
            returns a zoom level which may not have the best quality but will speed up
            reading significantly.
        min: Returns the zoom level which matches the minimum resolution of the extent's
            four corner pixels. This approach returns the zoom level with the best
            possible quality but with low performance. If the tile extent is outside of
            the destination pyramid, a TopologicalError will be raised.
    precision : int
        Round resolutions to n digits before comparing.

    Returns
    -------
    zoom : int
    """
    def width_height(bounds):
        try:
            l, b, r, t = reproject_geometry(
                box(*bounds), src_crs=tile.crs, dst_crs=dst_pyramid.crs
            ).bounds
        except ValueError:
            raise TopologicalError("bounds cannot be translated into target CRS")
        return r - l, t - b

    if tile.tp.crs == dst_pyramid.crs:
        return tile.zoom
    else:
        if matching_method == "gdal":
            # use rasterio/GDAL method to calculate default warp target properties
            transform, width, height = calculate_default_transform(
                tile.tp.crs,
                dst_pyramid.crs,
                tile.width,
                tile.height,
                *tile.bounds
            )
            # this is the resolution the tile would have in destination TilePyramid CRS
            tile_resolution = round(transform[0], precision)
        elif matching_method == "min":
            # calculate the minimum pixel size from the four tile corner pixels
            l, b, r, t = tile.bounds
            x = tile.pixel_x_size
            y = tile.pixel_y_size
            res = []
            for bounds in [
                (l, t - y, l + x, t),  # left top
                (l, b, l + x, b + y),  # left bottom
                (r - x, b, r, b + y),  # right bottom
                (r - x, t - y, r, t)   # right top
            ]:
                try:
                    w, h = width_height(bounds)
                    res.extend([w, h])
                except TopologicalError:
                    logger.debug("pixel outside of destination pyramid")
            if res:
                tile_resolution = round(min(res), precision)
            else:
                raise TopologicalError("tile outside of destination pyramid")
        else:
            raise ValueError("invalid method given: %s", matching_method)
        logger.debug(
            "we are looking for a zoom level interpolating to %s resolution",
            tile_resolution
        )
        zoom = 0
        while True:
            td_resolution = round(dst_pyramid.pixel_x_size(zoom), precision)
            if td_resolution <= tile_resolution:
                break
            zoom += 1
        logger.debug("target zoom for %s: %s (%s)", tile_resolution, zoom, td_resolution)
        return zoom