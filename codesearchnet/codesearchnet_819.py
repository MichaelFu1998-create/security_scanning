def _inhibitColumnsGlobal(self, overlaps, density):
    """
    Perform global inhibition. Performing global inhibition entails picking the
    top 'numActive' columns with the highest overlap score in the entire
    region. At most half of the columns in a local neighborhood are allowed to
    be active. Columns with an overlap score below the 'stimulusThreshold' are
    always inhibited.

    :param overlaps: an array containing the overlap score for each  column.
                    The overlap score for a column is defined as the number
                    of synapses in a "connected state" (connected synapses)
                    that are connected to input bits which are turned on.
    :param density: The fraction of columns to survive inhibition.
    @return list with indices of the winning columns
    """
    #calculate num active per inhibition area
    numActive = int(density * self._numColumns)

    # Calculate winners using stable sort algorithm (mergesort)
    # for compatibility with C++
    sortedWinnerIndices = numpy.argsort(overlaps, kind='mergesort')

    # Enforce the stimulus threshold
    start = len(sortedWinnerIndices) - numActive
    while start < len(sortedWinnerIndices):
      i = sortedWinnerIndices[start]
      if overlaps[i] >= self._stimulusThreshold:
        break
      else:
        start += 1

    return sortedWinnerIndices[start:][::-1]