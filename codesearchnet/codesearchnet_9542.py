def get_zoom_levels(process_zoom_levels=None, init_zoom_levels=None):
    """Validate and return zoom levels."""
    process_zoom_levels = _validate_zooms(process_zoom_levels)
    if init_zoom_levels is None:
        return process_zoom_levels
    else:
        init_zoom_levels = _validate_zooms(init_zoom_levels)
        if not set(init_zoom_levels).issubset(set(process_zoom_levels)):
            raise MapcheteConfigError(
                "init zooms must be a subset of process zoom")
        return init_zoom_levels