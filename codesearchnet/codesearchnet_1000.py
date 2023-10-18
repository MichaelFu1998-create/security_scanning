def _bitForCoordinate(cls, coordinate, n):
    """
    Maps the coordinate to a bit in the SDR.

    @param coordinate (numpy.array) Coordinate
    @param n (int) The number of available bits in the SDR
    @return (int) The index to a bit in the SDR
    """
    seed = cls._hashCoordinate(coordinate)
    rng = Random(seed)
    return rng.getUInt32(n)