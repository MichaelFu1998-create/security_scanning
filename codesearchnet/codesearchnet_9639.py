def segmentize_geometry(geometry, segmentize_value):
    """
    Segmentize Polygon outer ring by segmentize value.

    Just Polygon geometry type supported.

    Parameters
    ----------
    geometry : ``shapely.geometry``
    segmentize_value: float

    Returns
    -------
    geometry : ``shapely.geometry``
    """
    if geometry.geom_type != "Polygon":
        raise TypeError("segmentize geometry type must be Polygon")

    return Polygon(
        LinearRing([
            p
            # pick polygon linestrings
            for l in map(
                lambda x: LineString([x[0], x[1]]),
                zip(geometry.exterior.coords[:-1], geometry.exterior.coords[1:])
            )
            # interpolate additional points in between and don't forget end point
            for p in [
                l.interpolate(segmentize_value * i).coords[0]
                for i in range(int(l.length / segmentize_value))
            ] + [l.coords[1]]
        ])
    )