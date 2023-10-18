def multipart_to_singleparts(geom):
    """
    Yield single part geometries if geom is multipart, otherwise yield geom.

    Parameters:
    -----------
    geom : shapely geometry

    Returns:
    --------
    shapely single part geometries
    """
    if isinstance(geom, base.BaseGeometry):
        if hasattr(geom, "geoms"):
            for subgeom in geom:
                yield subgeom
        else:
            yield geom