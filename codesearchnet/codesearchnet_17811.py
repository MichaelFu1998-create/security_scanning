def matlab_formatter(level, vertices, codes=None):
    """`MATLAB`_ style contour formatter.

    Contours are returned as a single Nx2, `MATLAB`_ style, contour array.
    There are two types of rows in this format:

    * Header: The first element of a header row is the level of the contour
      (the lower level for filled contours) and the second element is the
      number of vertices (to follow) belonging to this contour line.
    * Vertex: x,y coordinate pairs of the vertex.

    A header row is always followed by the coresponding number of vertices.
    Another header row may follow if there are more contour lines.

    For filled contours the direction of vertices matters:

    * CCW (ACW): The vertices give the exterior of a contour polygon.
    * CW: The vertices give a hole of a contour polygon.  This hole will
        always be inside the exterior of the last contour exterior.

    For further explanation of this format see the `Mathworks documentation
    <https://www.mathworks.com/help/matlab/ref/contour-properties.html#prop_ContourMatrix>`_
    noting that the MATLAB format used in the `contours` package is the
    transpose of that used by `MATLAB`_ (since `MATLAB`_ is column-major
    and `NumPy`_ is row-major by default).

    .. _NumPy: http://www.numpy.org

    .. _MATLAB: https://www.mathworks.com/products/matlab.html

    """
    vertices = numpy_formatter(level, vertices, codes)
    if codes is not None:
        level = level[0]
    headers = np.vstack((
        [v.shape[0] for v in vertices],
        [level]*len(vertices))).T
    vertices = np.vstack(
        list(it.__next__() for it in
             itertools.cycle((iter(headers), iter(vertices)))))
    return vertices