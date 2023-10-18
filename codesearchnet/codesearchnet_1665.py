def printColConfidence(self, aState, maxCols = 20):
    """
    Print up to maxCols number from a flat floating point array.

    :param aState: TODO: document
    :param maxCols: TODO: document
    """
    def formatFPRow(var):
      s = ''
      for c in range(min(maxCols, self.numberOfCols)):
        if c > 0 and c % 10 == 0:
          s += '   '
        s += ' %5.3f' % var[c]
      s += ' '
      return s

    print formatFPRow(aState)