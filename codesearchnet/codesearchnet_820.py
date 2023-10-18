def _inhibitColumnsLocal(self, overlaps, density):
    """
    Performs local inhibition. Local inhibition is performed on a column by
    column basis. Each column observes the overlaps of its neighbors and is
    selected if its overlap score is within the top 'numActive' in its local
    neighborhood. At most half of the columns in a local neighborhood are
    allowed to be active. Columns with an overlap score below the
    'stimulusThreshold' are always inhibited.

    :param overlaps: an array containing the overlap score for each  column.
                    The overlap score for a column is defined as the number
                    of synapses in a "connected state" (connected synapses)
                    that are connected to input bits which are turned on.
    :param density: The fraction of columns to survive inhibition. This
                    value is only an intended target. Since the surviving
                    columns are picked in a local fashion, the exact fraction
                    of surviving columns is likely to vary.
    @return list with indices of the winning columns
    """

    activeArray = numpy.zeros(self._numColumns, dtype="bool")

    for column, overlap in enumerate(overlaps):
      if overlap >= self._stimulusThreshold:
        neighborhood = self._getColumnNeighborhood(column)
        neighborhoodOverlaps = overlaps[neighborhood]

        numBigger = numpy.count_nonzero(neighborhoodOverlaps > overlap)

        # When there is a tie, favor neighbors that are already selected as
        # active.
        ties = numpy.where(neighborhoodOverlaps == overlap)
        tiedNeighbors = neighborhood[ties]
        numTiesLost = numpy.count_nonzero(activeArray[tiedNeighbors])

        numActive = int(0.5 + density * len(neighborhood))
        if numBigger + numTiesLost < numActive:
          activeArray[column] = True

    return activeArray.nonzero()[0]