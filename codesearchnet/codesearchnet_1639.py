def mmPrettyPrintSequenceCellRepresentations(self, sortby="Column"):
    """
    Pretty print the cell representations for sequences in the history.

    @param sortby (string) Column of table to sort by

    @return (string) Pretty-printed text
    """
    self._mmComputeTransitionTraces()
    table = PrettyTable(["Pattern", "Column", "predicted=>active cells"])

    for sequenceLabel, predictedActiveCells in (
          self._mmData["predictedActiveCellsForSequence"].iteritems()):
      cellsForColumn = self.mapCellsToColumns(predictedActiveCells)
      for column, cells in cellsForColumn.iteritems():
        table.add_row([sequenceLabel, column, list(cells)])

    return table.get_string(sortby=sortby).encode("utf-8")