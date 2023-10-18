def _punishPredictedColumn(cls, connections, columnMatchingSegments,
                             prevActiveCells, predictedSegmentDecrement):
    """
    :param connections: (Object)
    Connections for the TM. Gets mutated.

    :param columnMatchingSegments: (iter)
    Matching segments for this column.

    :param prevActiveCells: (list)
    Active cells in `t-1`.

    :param predictedSegmentDecrement: (float)
    Amount by which segments are punished for incorrect predictions.

    Pseudocode:
    for each matching segment in the column
      weaken active synapses
    """
    if predictedSegmentDecrement > 0.0 and columnMatchingSegments is not None:
      for segment in columnMatchingSegments:
        cls._adaptSegment(connections, segment, prevActiveCells,
                          -predictedSegmentDecrement, 0.0)