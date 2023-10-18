def shapely_formatter(_, vertices, codes=None):
    """`Shapely`_ style contour formatter.

    Contours are returned as a list of :class:`shapely.geometry.LineString`,
    :class:`shapely.geometry.LinearRing`, and :class:`shapely.geometry.Point`
    geometry elements.

    Filled contours return a list of :class:`shapely.geometry.Polygon`
    elements instead.

    .. note:: If possible, `Shapely speedups`_ will be enabled.

    .. _Shapely: http://toblerity.org/shapely/manual.html

    .. _Shapely speedups: http://toblerity.org/shapely/manual.html#performance


    See Also
    --------
    `descartes <https://bitbucket.org/sgillies/descartes/>`_ : Use `Shapely`_
    or GeoJSON-like geometric objects as matplotlib paths and patches.

    """
    elements = []
    if codes is None:
        for vertices_ in vertices:
            if np.all(vertices_[0, :] == vertices_[-1, :]):
                # Contour is single point.
                if len(vertices) < 3:
                    elements.append(Point(vertices_[0, :]))
                # Contour is closed.
                else:
                    elements.append(LinearRing(vertices_))
            # Contour is open.
            else:
                elements.append(LineString(vertices_))
    else:
        for vertices_, codes_ in zip(vertices, codes):
            starts = np.nonzero(codes_ == MPLPATHCODE.MOVETO)[0]
            stops = np.nonzero(codes_ == MPLPATHCODE.CLOSEPOLY)[0]
            try:
                rings = [LinearRing(vertices_[start:stop+1, :])
                        for start, stop in zip(starts, stops)]
                elements.append(Polygon(rings[0], rings[1:]))
            except ValueError as err:
                # Verify error is from degenerate (single point) polygon.
                if np.any(stop - start - 1 == 0):
                    # Polygon is single point, remove the polygon.
                    if stops[0] < starts[0]+2:
                        pass
                    # Polygon has single point hole, remove the hole.
                    else:
                        rings = [
                            LinearRing(vertices_[start:stop+1, :])
                            for start, stop in zip(starts, stops)
                            if stop >= start+2]
                        elements.append(Polygon(rings[0], rings[1:]))
                else:
                    raise(err)
    return elements