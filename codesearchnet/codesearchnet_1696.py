def _getBestMatchingCell(self, c, activeState, minThreshold):
    """
    Find weakly activated cell in column with at least minThreshold active
    synapses.

    :param c            which column to look at
    :param activeState  the active cells
    :param minThreshold minimum number of synapses required

    :returns: tuple (cellIdx, segment, numActiveSynapses)
    """
    # Collect all cells in column c that have at least minThreshold in the most
    # activated segment
    bestActivityInCol = minThreshold
    bestSegIdxInCol = -1
    bestCellInCol = -1

    for i in xrange(self.cellsPerColumn):

      maxSegActivity = 0
      maxSegIdx = 0

      for j, s in enumerate(self.cells[c][i]):

        activity = self._getSegmentActivityLevel(s, activeState)

        if activity > maxSegActivity:
          maxSegActivity = activity
          maxSegIdx = j

      if maxSegActivity >= bestActivityInCol:
        bestActivityInCol = maxSegActivity
        bestSegIdxInCol = maxSegIdx
        bestCellInCol = i

    if bestCellInCol == -1:
      return (None, None, None)
    else:
      return (bestCellInCol, self.cells[c][bestCellInCol][bestSegIdxInCol],
                bestActivityInCol)