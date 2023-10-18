def _inferPhase2(self):
    """
    Phase 2 for the inference state. The computes the predicted state, then
    checks to insure that the predicted state is not over-saturated, i.e.
    look too close like a burst. This indicates that there were so many
    separate paths learned from the current input columns to the predicted
    input columns that bursting on the current input columns is most likely
    generated mix and match errors on cells in the predicted columns. If
    we detect this situation, we instead turn on only the start cells in the
    current active columns and re-generate the predicted state from those.

    This looks at:
        - `` infActiveState['t']``

    This modifies:
        - `` infPredictedState['t']``
        - `` colConfidence['t']``
        - `` cellConfidence['t']``

    :returns: (bool) True if we have a decent guess as to the next input.
              Returning False from here indicates to the caller that we have
              reached the end of a learned sequence.
    """
    # Init to zeros to start
    self.infPredictedState['t'].fill(0)
    self.cellConfidence['t'].fill(0)
    self.colConfidence['t'].fill(0)

    # Phase 2 - Compute new predicted state and update cell and column
    #   confidences
    for c in xrange(self.numberOfCols):

      # For each cell in the column
      for i in xrange(self.cellsPerColumn):

        # For each segment in the cell
        for s in self.cells[c][i]:

          # See if it has the min number of active synapses
          numActiveSyns = self._getSegmentActivityLevel(
              s, self.infActiveState['t'], connectedSynapsesOnly=False)
          if numActiveSyns < self.activationThreshold:
            continue

          # Incorporate the confidence into the owner cell and column
          if self.verbosity >= 6:
            print "incorporating DC from cell[%d,%d]:   " % (c, i),
            s.debugPrint()
          dc = s.dutyCycle()
          self.cellConfidence['t'][c, i] += dc
          self.colConfidence['t'][c] += dc

          # If we reach threshold on the connected synapses, predict it
          # If not active, skip over it
          if self._isSegmentActive(s, self.infActiveState['t']):
            self.infPredictedState['t'][c, i] = 1

    # Normalize column and cell confidences
    sumConfidences = self.colConfidence['t'].sum()
    if sumConfidences > 0:
      self.colConfidence['t'] /= sumConfidences
      self.cellConfidence['t'] /= sumConfidences

    # Are we predicting the required minimum number of columns?
    numPredictedCols = self.infPredictedState['t'].max(axis=1).sum()
    if numPredictedCols >= 0.5 * self.avgInputDensity:
      return True
    else:
      return False