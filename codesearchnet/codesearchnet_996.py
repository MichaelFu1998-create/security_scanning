def _neighbors(coordinate, radius):
    """
    Returns coordinates around given coordinate, within given radius.
    Includes given coordinate.

    @param coordinate (numpy.array) N-dimensional integer coordinate
    @param radius (int) Radius around `coordinate`

    @return (numpy.array) List of coordinates
    """
    ranges = (xrange(n-radius, n+radius+1) for n in coordinate.tolist())
    return numpy.array(list(itertools.product(*ranges)))