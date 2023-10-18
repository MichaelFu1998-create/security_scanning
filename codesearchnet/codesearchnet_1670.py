def printActiveIndices(self, state, andValues=False):
    """
    Print the list of ``[column, cellIdx]`` indices for each of the active cells 
    in state.

    :param state: TODO: document
    :param andValues: TODO: document
    """
    if len(state.shape) == 2:
      (cols, cellIdxs) = state.nonzero()
    else:
      cols = state.nonzero()[0]
      cellIdxs = numpy.zeros(len(cols))

    if len(cols) == 0:
      print "NONE"
      return

    prevCol = -1
    for (col, cellIdx) in zip(cols, cellIdxs):
      if col != prevCol:
        if prevCol != -1:
          print "] ",
        print "Col %d: [" % (col),
        prevCol = col

      if andValues:
        if len(state.shape) == 2:
          value = state[col, cellIdx]
        else:
          value = state[col]
        print "%d: %s," % (cellIdx, value),
      else:
        print "%d," % (cellIdx),
    print "]"