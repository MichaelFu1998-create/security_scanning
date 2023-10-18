def _burstColumn(cls, connections, random, lastUsedIterationForSegment,
                   column, columnMatchingSegments, prevActiveCells,
                   prevWinnerCells, cellsForColumn,
                   numActivePotentialSynapsesForSegment, iteration,
                   maxNewSynapseCount, initialPermanence, permanenceIncrement,
                   permanenceDecrement, maxSegmentsPerCell,
                   maxSynapsesPerSegment, learn):
    """
    :param connections: (Object)
    Connections for the TM. Gets mutated.

    :param random: (Object)
    Random number generator. Gets mutated.

    :param lastUsedIterationForSegment: (list)
    Last used iteration for each segment, indexed by the segment's flatIdx.
    Gets mutated.

    :param column: (int)
    Index of bursting column.

    :param columnMatchingSegments: (iter)
    Matching segments in this column.

    :param prevActiveCells: (list)
    Active cells in `t-1`.

    :param prevWinnerCells: (list)
    Winner cells in `t-1`.

    :param cellsForColumn: (sequence)
    Range of cell indices on which to operate.

    :param numActivePotentialSynapsesForSegment: (list)
    Number of active potential synapses per segment, indexed by the segment's
    flatIdx.

    :param iteration: (int)
    The current timestep.

    :param maxNewSynapseCount: (int)
    The maximum number of synapses added to a segment during learning.

    :param initialPermanence: (float)
    Initial permanence of a new synapse.

    :param permanenceIncrement: (float)
    Amount by which permanences of synapses are incremented during learning.

    :param permanenceDecrement: (float)
    Amount by which permanences of synapses are decremented during learning.

    :param maxSegmentsPerCell: (int)
    The maximum number of segments per cell.

    :param maxSynapsesPerSegment: (int)
    The maximum number of synapses per segment.

    :param learn: (bool)
    Whether or not learning is enabled.

    :returns: (tuple) Contains:
                      `cells`         (iter),
                      `winnerCell`    (int),

    Pseudocode:
    mark all cells as active
    if there are any matching distal dendrite segments
      find the most active matching segment
      mark its cell as a winner cell
      (learning)
        grow and reinforce synapses to previous winner cells
    else
      find the cell with the least segments, mark it as a winner cell
      (learning)
        (optimization) if there are prev winner cells
          add a segment to this winner cell
          grow synapses to previous winner cells
    """
    if columnMatchingSegments is not None:
      numActive = lambda s: numActivePotentialSynapsesForSegment[s.flatIdx]
      bestMatchingSegment = max(columnMatchingSegments, key=numActive)
      winnerCell = bestMatchingSegment.cell

      if learn:
        cls._adaptSegment(connections, bestMatchingSegment, prevActiveCells,
                          permanenceIncrement, permanenceDecrement)

        nGrowDesired = maxNewSynapseCount - numActive(bestMatchingSegment)

        if nGrowDesired > 0:
          cls._growSynapses(connections, random, bestMatchingSegment,
                            nGrowDesired, prevWinnerCells, initialPermanence,
                            maxSynapsesPerSegment)
    else:
      winnerCell = cls._leastUsedCell(random, cellsForColumn, connections)
      if learn:
        nGrowExact = min(maxNewSynapseCount, len(prevWinnerCells))
        if nGrowExact > 0:
          segment = cls._createSegment(connections,
                                       lastUsedIterationForSegment, winnerCell,
                                       iteration, maxSegmentsPerCell)
          cls._growSynapses(connections, random, segment, nGrowExact,
                            prevWinnerCells, initialPermanence,
                            maxSynapsesPerSegment)

    return cellsForColumn, winnerCell