def activatePredictedColumn(self, column, columnActiveSegments,
                              columnMatchingSegments, prevActiveCells,
                              prevWinnerCells, learn):
    """
    Determines which cells in a predicted column should be added to winner cells
    list, and learns on the segments that correctly predicted this column.

    :param column: (int) Index of bursting column.

    :param columnActiveSegments: (iter) Active segments in this column.

    :param columnMatchingSegments: (iter) Matching segments in this column.

    :param prevActiveCells: (list) Active cells in ``t-1``.

    :param prevWinnerCells: (list) Winner cells in ``t-1``.

    :param learn: (bool) If true, grow and reinforce synapses.

    :returns: (list) A list of predicted cells that will be added to 
              active cells and winner cells.
    """
    return self._activatePredictedColumn(
      self.connections, self._random,
      columnActiveSegments, prevActiveCells, prevWinnerCells,
      self.numActivePotentialSynapsesForSegment,
      self.maxNewSynapseCount, self.initialPermanence,
      self.permanenceIncrement, self.permanenceDecrement,
      self.maxSynapsesPerSegment, learn)