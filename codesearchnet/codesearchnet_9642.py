def clean_geometry_type(geometry, target_type, allow_multipart=True):
    """
    Return geometry of a specific type if possible.

    Filters and splits up GeometryCollection into target types. This is
    necessary when after clipping and/or reprojecting the geometry types from
    source geometries change (i.e. a Polygon becomes a LineString or a
    LineString becomes Point) in some edge cases.

    Parameters
    ----------
    geometry : ``shapely.geometry``
    target_type : string
        target geometry type
    allow_multipart : bool
        allow multipart geometries (default: True)

    Returns
    -------
    cleaned geometry : ``shapely.geometry``
        returns None if input geometry type differs from target type

    Raises
    ------
    GeometryTypeError : if geometry type does not match target_type
    """
    multipart_geoms = {
        "Point": MultiPoint,
        "LineString": MultiLineString,
        "Polygon": MultiPolygon,
        "MultiPoint": MultiPoint,
        "MultiLineString": MultiLineString,
        "MultiPolygon": MultiPolygon
    }

    if target_type not in multipart_geoms.keys():
        raise TypeError("target type is not supported: %s" % target_type)

    if geometry.geom_type == target_type:
        return geometry

    elif allow_multipart:
        target_multipart_type = multipart_geoms[target_type]
        if geometry.geom_type == "GeometryCollection":
            return target_multipart_type([
                clean_geometry_type(g, target_type, allow_multipart)
                for g in geometry])
        elif any([
            isinstance(geometry, target_multipart_type),
            multipart_geoms[geometry.geom_type] == target_multipart_type
        ]):
            return geometry

    raise GeometryTypeError(
        "geometry type does not match: %s, %s" % (geometry.geom_type, target_type)
    )