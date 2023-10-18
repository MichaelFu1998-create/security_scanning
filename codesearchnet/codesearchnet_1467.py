def punishPredictedColumn(self, column, columnActiveSegments,
                            columnMatchingSegments, prevActiveCells,
                            prevWinnerCells):
    """
    Punishes the Segments that incorrectly predicted a column to be active.

    :param column: (int) Index of bursting column.

    :param columnActiveSegments: (iter) Active segments for this column, or None 
           if there aren't any.

    :param columnMatchingSegments: (iter) Matching segments for this column, or 
           None if there aren't any.

    :param prevActiveCells: (list) Active cells in ``t-1``.

    :param prevWinnerCells: (list) Winner cells in ``t-1``.

    """
    self._punishPredictedColumn(
      self.connections, columnMatchingSegments, prevActiveCells,
      self.predictedSegmentDecrement)