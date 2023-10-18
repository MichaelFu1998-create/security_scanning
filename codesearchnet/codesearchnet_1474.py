def _leastUsedCell(cls, random, cells, connections):
    """
    Gets the cell with the smallest number of segments.
    Break ties randomly.

    :param random: (Object)
    Random number generator. Gets mutated.

    :param cells: (list)
    Indices of cells.

    :param connections: (Object)
    Connections instance for the TM.

    :returns: (int) Cell index.
    """
    leastUsedCells = []
    minNumSegments = float("inf")
    for cell in cells:
      numSegments = connections.numSegments(cell)

      if numSegments < minNumSegments:
        minNumSegments = numSegments
        leastUsedCells = []

      if numSegments == minNumSegments:
        leastUsedCells.append(cell)

    i = random.getUInt32(len(leastUsedCells))
    return leastUsedCells[i]