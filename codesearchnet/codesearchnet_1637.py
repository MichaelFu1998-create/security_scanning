def mmGetMetricSequencesPredictedActiveCellsShared(self):
    """
    Metric for number of sequences each predicted => active cell appears in

    Note: This metric is flawed when it comes to high-order sequences.

    @return (Metric) metric
    """
    self._mmComputeTransitionTraces()

    numSequencesForCell = defaultdict(lambda: 0)

    for predictedActiveCells in (
          self._mmData["predictedActiveCellsForSequence"].values()):
      for cell in predictedActiveCells:
        numSequencesForCell[cell] += 1

    return Metric(self,
                  "# sequences each predicted => active cells appears in",
                  numSequencesForCell.values())