def _validate_zooms(zooms):
    """
    Return a list of zoom levels.

    Following inputs are converted:
    - int --> [int]
    - dict{min, max} --> range(min, max + 1)
    - [int] --> [int]
    - [int, int] --> range(smaller int, bigger int + 1)
    """
    if isinstance(zooms, dict):
        if any([a not in zooms for a in ["min", "max"]]):
            raise MapcheteConfigError("min and max zoom required")
        zmin = _validate_zoom(zooms["min"])
        zmax = _validate_zoom(zooms["max"])
        if zmin > zmax:
            raise MapcheteConfigError(
                "max zoom must not be smaller than min zoom")
        return list(range(zmin, zmax + 1))
    elif isinstance(zooms, list):
        if len(zooms) == 1:
            return zooms
        elif len(zooms) == 2:
            zmin, zmax = sorted([_validate_zoom(z) for z in zooms])
            return list(range(zmin, zmax + 1))
        else:
            return zooms
    else:
        return [_validate_zoom(zooms)]