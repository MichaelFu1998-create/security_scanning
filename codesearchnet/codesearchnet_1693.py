def trimSegments(self, minPermanence=None, minNumSyns=None):
    """
    This method deletes all synapses whose permanence is less than
    minPermanence and deletes any segments that have less than
    minNumSyns synapses remaining.

    :param minPermanence: (float) Any syn whose permanence is 0 or < 
           ``minPermanence``  will be deleted. If None is passed in, then 
           ``self.connectedPerm`` is used.
    :param minNumSyns: (int) Any segment with less than ``minNumSyns`` synapses 
           remaining in it will be deleted. If None is passed in, then 
           ``self.activationThreshold`` is used.
    :returns: (tuple) ``numSegsRemoved``, ``numSynsRemoved``
    """
    # Fill in defaults
    if minPermanence is None:
      minPermanence = self.connectedPerm
    if minNumSyns is None:
      minNumSyns = self.activationThreshold

    # Loop through all cells
    totalSegsRemoved, totalSynsRemoved = 0, 0
    for c, i in itertools.product(xrange(self.numberOfCols),
                                  xrange(self.cellsPerColumn)):

      (segsRemoved, synsRemoved) = self._trimSegmentsInCell(
          colIdx=c, cellIdx=i, segList=self.cells[c][i],
          minPermanence=minPermanence, minNumSyns=minNumSyns)
      totalSegsRemoved += segsRemoved
      totalSynsRemoved += synsRemoved

    # Print all cells if verbosity says to
    if self.verbosity >= 5:
      print "Cells, all segments:"
      self.printCells(predictedOnly=False)

    return totalSegsRemoved, totalSynsRemoved