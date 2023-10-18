def _orderForCoordinate(cls, coordinate):
    """
    Returns the order for a coordinate.

    @param coordinate (numpy.array) Coordinate
    @return (float) A value in the interval [0, 1), representing the
                    order of the coordinate
    """
    seed = cls._hashCoordinate(coordinate)
    rng = Random(seed)
    return rng.getReal64()