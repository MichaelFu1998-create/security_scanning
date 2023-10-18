def _activatePredictedColumn(cls, connections, random, columnActiveSegments,
                               prevActiveCells, prevWinnerCells,
                               numActivePotentialSynapsesForSegment,
                               maxNewSynapseCount, initialPermanence,
                               permanenceIncrement, permanenceDecrement,
                               maxSynapsesPerSegment, learn):
    """
    :param connections: (Object)
    Connections for the TM. Gets mutated.

    :param random: (Object)
    Random number generator. Gets mutated.

    :param columnActiveSegments: (iter)
    Active segments in this column.

    :param prevActiveCells: (list)
    Active cells in `t-1`.

    :param prevWinnerCells: (list)
    Winner cells in `t-1`.

    :param numActivePotentialSynapsesForSegment: (list)
    Number of active potential synapses per segment, indexed by the segment's
    flatIdx.

    :param maxNewSynapseCount: (int)
    The maximum number of synapses added to a segment during learning

    :param initialPermanence: (float)
    Initial permanence of a new synapse.

    @permanenceIncrement (float)
    Amount by which permanences of synapses are incremented during learning.

    @permanenceDecrement (float)
    Amount by which permanences of synapses are decremented during learning.

    :param maxSynapsesPerSegment: (int)
    The maximum number of synapses per segment.

    :param learn: (bool)
    If true, grow and reinforce synapses.

    :returns: cellsToAdd (list)
    A list of predicted cells that will be added to active cells and winner
    cells.

    Pseudocode:
    for each cell in the column that has an active distal dendrite segment
      mark the cell as active
      mark the cell as a winner cell
      (learning) for each active distal dendrite segment
        strengthen active synapses
        weaken inactive synapses
        grow synapses to previous winner cells
    """

    cellsToAdd = []
    previousCell = None
    for segment in columnActiveSegments:
      if segment.cell != previousCell:
        cellsToAdd.append(segment.cell)
        previousCell = segment.cell

      if learn:
        cls._adaptSegment(connections, segment, prevActiveCells,
                          permanenceIncrement, permanenceDecrement)

        active = numActivePotentialSynapsesForSegment[segment.flatIdx]
        nGrowDesired = maxNewSynapseCount - active

        if nGrowDesired > 0:
          cls._growSynapses(connections, random, segment, nGrowDesired,
                            prevWinnerCells, initialPermanence,
                            maxSynapsesPerSegment)

    return cellsToAdd