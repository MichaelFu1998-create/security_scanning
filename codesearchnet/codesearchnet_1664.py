def printConfidence(self, aState, maxCols = 20):
    """
    Print a floating point array that is the same shape as activeState.

    :param aState: TODO: document
    :param maxCols: TODO: document
    """
    def formatFPRow(var, i):
      s = ''
      for c in range(min(maxCols, self.numberOfCols)):
        if c > 0 and c % 10 == 0:
          s += '   '
        s += ' %5.3f' % var[c, i]
      s += ' '
      return s

    for i in xrange(self.cellsPerColumn):
      print formatFPRow(aState, i)