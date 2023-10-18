def numpy_formatter(_, vertices, codes=None):
    """`NumPy`_ style contour formatter.

    Contours are returned as a list of Nx2 arrays containing the x and y
    vertices of the contour line.

    For filled contours the direction of vertices matters:

    * CCW (ACW): The vertices give the exterior of a contour polygon.
    * CW: The vertices give a hole of a contour polygon.  This hole will
        always be inside the exterior of the last contour exterior.

    .. note:: This is the fastest format.

    .. _NumPy: http://www.numpy.org

    """
    if codes is None:
        return vertices
    numpy_vertices = []
    for vertices_, codes_ in zip(vertices, codes):
        starts = np.nonzero(codes_ == MPLPATHCODE.MOVETO)[0]
        stops = np.nonzero(codes_ == MPLPATHCODE.CLOSEPOLY)[0]
        for start, stop in zip(starts, stops):
            numpy_vertices.append(vertices_[start:stop+1, :])
    return numpy_vertices