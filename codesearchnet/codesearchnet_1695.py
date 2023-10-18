def finishLearning(self):
    """
    Called when learning has been completed. This method just calls
    :meth:`trimSegments` and then clears out caches.
    """
    # Keep weakly formed synapses around because they contain confidence scores
    # for paths out of learned sequenced and produce a better prediction than
    # chance.
    self.trimSegments(minPermanence=0.0001)

    # Update all cached duty cycles for better performance right after loading
    # in the trained network.
    for c, i in itertools.product(xrange(self.numberOfCols),
                                  xrange(self.cellsPerColumn)):
      for segment in self.cells[c][i]:
        segment.dutyCycle()

    # For error checking purposes, make sure no start cell has incoming
    # connections
    if self.cellsPerColumn > 1:
      for c in xrange(self.numberOfCols):
        assert self.getNumSegmentsInCell(c, 0) == 0