def _initEphemerals(self):
    """
    Initialize all ephemerals used by derived classes.
    """

    if hasattr(self, '_sfdr') and self._sfdr:
      self._spatialPoolerOutput = numpy.zeros(self.columnCount,
                                               dtype=GetNTAReal())
    else:
      self._spatialPoolerOutput = None  # Will be filled in initInNetwork

    # Direct logging support (faster than node watch)
    self._fpLogSPInput = None
    self._fpLogSP = None
    self._fpLogSPDense = None
    self.logPathInput = ""
    self.logPathOutput = ""
    self.logPathOutputDense = ""