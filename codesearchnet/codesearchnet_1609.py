def trimSegments(self, minPermanence=None, minNumSyns=None):
    """
    Overrides :meth:`nupic.algorithms.backtracking_tm.BacktrackingTM.trimSegments`.
    """
    # Fill in defaults
    if minPermanence is None:
      minPermanence = 0.0
    if minNumSyns is None:
      minNumSyns = 0

    # Print all cells if verbosity says to
    if self.verbosity >= 5:
      print "Cells, all segments:"
      self.printCells(predictedOnly=False)

    return self.cells4.trimSegments(minPermanence=minPermanence, minNumSyns=minNumSyns)