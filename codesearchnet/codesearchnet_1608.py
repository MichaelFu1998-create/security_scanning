def reset(self):
    """
    Overrides :meth:`nupic.algorithms.backtracking_tm.BacktrackingTM.reset`.
    """
    if self.verbosity >= 3:
      print "TM Reset"
    self._setStatePointers()
    self.cells4.reset()
    BacktrackingTM.reset(self)