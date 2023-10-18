def initialize(self):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.initialize`.
    """
    # Zero out the spatial output in case it is requested
    self._spatialPoolerOutput = numpy.zeros(self.columnCount,
                                            dtype=GetNTAReal())

    # Zero out the rfInput in case it is requested
    self._spatialPoolerInput = numpy.zeros((1, self.inputWidth),
                                           dtype=GetNTAReal())

    # Allocate the spatial pooler
    self._allocateSpatialFDR(None)