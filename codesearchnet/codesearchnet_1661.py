def reset(self,):
    """
    Reset the state of all cells.

    This is normally used between sequences while training. All internal states
    are reset to 0.
    """
    if self.verbosity >= 3:
      print "\n==== RESET ====="

    self.lrnActiveState['t-1'].fill(0)
    self.lrnActiveState['t'].fill(0)
    self.lrnPredictedState['t-1'].fill(0)
    self.lrnPredictedState['t'].fill(0)

    self.infActiveState['t-1'].fill(0)
    self.infActiveState['t'].fill(0)
    self.infPredictedState['t-1'].fill(0)
    self.infPredictedState['t'].fill(0)

    self.cellConfidence['t-1'].fill(0)
    self.cellConfidence['t'].fill(0)

    # Flush the segment update queue
    self.segmentUpdates = {}

    self._internalStats['nInfersSinceReset'] = 0

    #To be removed
    self._internalStats['curPredictionScore'] = 0
    #New prediction score
    self._internalStats['curPredictionScore2']   = 0
    self._internalStats['curFalseNegativeScore'] = 0
    self._internalStats['curFalsePositiveScore'] = 0

    self._internalStats['curMissing'] = 0
    self._internalStats['curExtra'] = 0

    # When a reset occurs, set prevSequenceSignature to the signature of the
    # just-completed sequence and start accumulating histogram for the next
    # sequence.
    self._internalStats['prevSequenceSignature'] = None
    if self.collectSequenceStats:
      if self._internalStats['confHistogram'].sum() > 0:
        sig = self._internalStats['confHistogram'].copy()
        sig.reshape(self.numberOfCols * self.cellsPerColumn)
        self._internalStats['prevSequenceSignature'] = sig
      self._internalStats['confHistogram'].fill(0)

    self.resetCalled = True

    # Clear out input history
    self._prevInfPatterns = []
    self._prevLrnPatterns = []