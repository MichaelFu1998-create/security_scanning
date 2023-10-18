def printState(self, aState):
    """
    Print an integer array that is the same shape as activeState.

    :param aState: TODO: document
    """
    def formatRow(var, i):
      s = ''
      for c in range(self.numberOfCols):
        if c > 0 and c % 10 == 0:
          s += ' '
        s += str(var[c, i])
      s += ' '
      return s

    for i in xrange(self.cellsPerColumn):
      print formatRow(aState, i)