def encodeIntoArray(self, inputData, output):
    """
    See `nupic.encoders.base.Encoder` for more information.

    @param inputData (tuple) Contains coordinate (numpy.array, N-dimensional
                             integer coordinate) and radius (int)
    @param output (numpy.array) Stores encoded SDR in this numpy array
    """
    (coordinate, radius) = inputData

    assert isinstance(radius, int), ("Expected integer radius, got: {} ({})"
                                     .format(radius, type(radius)))

    neighbors = self._neighbors(coordinate, radius)
    winners = self._topWCoordinates(neighbors, self.w)

    bitFn = lambda coordinate: self._bitForCoordinate(coordinate, self.n)
    indices = numpy.array([bitFn(w) for w in winners])

    output[:] = 0
    output[indices] = 1