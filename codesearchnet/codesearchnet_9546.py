def bounds_from_opts(
    wkt_geometry=None, point=None, bounds=None, zoom=None, raw_conf=None
):
    """
    Loads the process pyramid of a raw configuration.

    Parameters
    ----------
    raw_conf : dict
        Raw mapchete configuration as dictionary.

    Returns
    -------
    BufferedTilePyramid
    """
    if wkt_geometry:
        return wkt.loads(wkt_geometry).bounds
    elif point:
        x, y = point
        zoom_levels = get_zoom_levels(
            process_zoom_levels=raw_conf["zoom_levels"],
            init_zoom_levels=zoom
        )
        tp = raw_conf_process_pyramid(raw_conf)
        return tp.tile_from_xy(x, y, max(zoom_levels)).bounds
    else:
        return bounds