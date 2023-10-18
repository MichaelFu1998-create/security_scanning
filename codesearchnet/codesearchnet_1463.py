def activateCells(self, activeColumns, learn=True):
    """
    Calculate the active cells, using the current active columns and dendrite
    segments. Grow and reinforce synapses.

    :param activeColumns: (iter) A sorted list of active column indices.

    :param learn: (bool) If true, reinforce / punish / grow synapses.

      **Pseudocode:**
      
      ::

        for each column
          if column is active and has active distal dendrite segments
            call activatePredictedColumn
          if column is active and doesn't have active distal dendrite segments
            call burstColumn
          if column is inactive and has matching distal dendrite segments
            call punishPredictedColumn
    """
    prevActiveCells = self.activeCells
    prevWinnerCells = self.winnerCells
    self.activeCells = []
    self.winnerCells = []

    segToCol = lambda segment: int(segment.cell / self.cellsPerColumn)
    identity = lambda x: x

    for columnData in groupby2(activeColumns, identity,
                               self.activeSegments, segToCol,
                               self.matchingSegments, segToCol):
      (column,
       activeColumns,
       columnActiveSegments,
       columnMatchingSegments) = columnData
      if activeColumns is not None:
        if columnActiveSegments is not None:
          cellsToAdd = self.activatePredictedColumn(column,
                                                    columnActiveSegments,
                                                    columnMatchingSegments,
                                                    prevActiveCells,
                                                    prevWinnerCells,
                                                    learn)

          self.activeCells += cellsToAdd
          self.winnerCells += cellsToAdd
        else:
          (cellsToAdd,
           winnerCell) = self.burstColumn(column,
                                          columnMatchingSegments,
                                          prevActiveCells,
                                          prevWinnerCells,
                                          learn)

          self.activeCells += cellsToAdd
          self.winnerCells.append(winnerCell)
      else:
        if learn:
          self.punishPredictedColumn(column,
                                     columnActiveSegments,
                                     columnMatchingSegments,
                                     prevActiveCells,
                                     prevWinnerCells)