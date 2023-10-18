def _topWCoordinates(cls, coordinates, w):
    """
    Returns the top W coordinates by order.

    @param coordinates (numpy.array) A 2D numpy array, where each element
                                     is a coordinate
    @param w (int) Number of top coordinates to return
    @return (numpy.array) A subset of `coordinates`, containing only the
                          top ones by order
    """
    orders = numpy.array([cls._orderForCoordinate(c)
                          for c in coordinates.tolist()])
    indices = numpy.argsort(orders)[-w:]
    return coordinates[indices]