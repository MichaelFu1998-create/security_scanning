def _updateInferenceState(self, activeColumns):
    """
    Update the inference state. Called from :meth:`compute` on every iteration.

    :param activeColumns: (list) active column indices.
    """
    # Copy t to t-1
    self.infActiveState['t-1'][:, :] = self.infActiveState['t'][:, :]
    self.infPredictedState['t-1'][:, :] = self.infPredictedState['t'][:, :]
    self.cellConfidence['t-1'][:, :] = self.cellConfidence['t'][:, :]
    self.colConfidence['t-1'][:] = self.colConfidence['t'][:]

    # Each phase will zero/initilize the 't' states that it affects

    # Update our inference input history
    if self.maxInfBacktrack > 0:
      if len(self._prevInfPatterns) > self.maxInfBacktrack:
        self._prevInfPatterns.pop(0)
      self._prevInfPatterns.append(activeColumns)

    # Compute the active state given the predictions from last time step and
    # the current bottom-up
    inSequence = self._inferPhase1(activeColumns, self.resetCalled)

    # If this input was considered unpredicted, let's go back in time and
    # replay the recent inputs from start cells and see if we can lock onto
    # this current set of inputs that way.
    if not inSequence:
      if self.verbosity >= 3:
        print ("Too much unpredicted input, re-tracing back to try and lock on "
               "at an earlier timestep.")
      # inferBacktrack() will call inferPhase2() for us.
      self._inferBacktrack(activeColumns)
      return

    # Compute the predicted cells and the cell and column confidences
    inSequence = self._inferPhase2()
    if not inSequence:
      if self.verbosity >= 3:
        print ("Not enough predictions going forward, "
               "re-tracing back to try and lock on at an earlier timestep.")
      # inferBacktrack() will call inferPhase2() for us.
      self._inferBacktrack(activeColumns)