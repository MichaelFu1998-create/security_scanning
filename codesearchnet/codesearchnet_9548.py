def _raw_at_zoom(config, zooms):
    """Return parameter dictionary per zoom level."""
    params_per_zoom = {}
    for zoom in zooms:
        params = {}
        for name, element in config.items():
            if name not in _RESERVED_PARAMETERS:
                out_element = _element_at_zoom(name, element, zoom)
                if out_element is not None:
                    params[name] = out_element
        params_per_zoom[zoom] = params
    return params_per_zoom