def mmGetMetricSequencesPredictedActiveCellsPerColumn(self):
    """
    Metric for number of predicted => active cells per column for each sequence

    @return (Metric) metric
    """
    self._mmComputeTransitionTraces()

    numCellsPerColumn = []

    for predictedActiveCells in (
        self._mmData["predictedActiveCellsForSequence"].values()):
      cellsForColumn = self.mapCellsToColumns(predictedActiveCells)
      numCellsPerColumn += [len(x) for x in cellsForColumn.values()]

    return Metric(self,
                  "# predicted => active cells per column for each sequence",
                  numCellsPerColumn)