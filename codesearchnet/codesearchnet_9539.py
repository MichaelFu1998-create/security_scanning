def _get_zoom(zoom, input_raster, pyramid_type):
    """Determine minimum and maximum zoomlevel."""
    if not zoom:
        minzoom = 1
        maxzoom = get_best_zoom_level(input_raster, pyramid_type)
    elif len(zoom) == 1:
        minzoom = zoom[0]
        maxzoom = zoom[0]
    elif len(zoom) == 2:
        if zoom[0] < zoom[1]:
            minzoom = zoom[0]
            maxzoom = zoom[1]
        else:
            minzoom = zoom[1]
            maxzoom = zoom[0]
    return minzoom, maxzoom