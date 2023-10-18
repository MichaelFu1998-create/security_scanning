def _updateLearningState(self, activeColumns):
    """
    Update the learning state. Called from compute() on every iteration
    :param activeColumns List of active column indices
    """
    # Copy predicted and active states into t-1
    self.lrnPredictedState['t-1'][:, :] = self.lrnPredictedState['t'][:, :]
    self.lrnActiveState['t-1'][:, :] = self.lrnActiveState['t'][:, :]

    # Update our learning input history
    if self.maxLrnBacktrack > 0:
      if len(self._prevLrnPatterns) > self.maxLrnBacktrack:
        self._prevLrnPatterns.pop(0)
      self._prevLrnPatterns.append(activeColumns)
      if self.verbosity >= 4:
        print "Previous learn patterns: \n"
        print self._prevLrnPatterns

    # Process queued up segment updates, now that we have bottom-up, we
    # can update the permanences on the cells that we predicted to turn on
    # and did receive bottom-up
    self._processSegmentUpdates(activeColumns)

    # Decrement the PAM counter if it is running and increment our learned
    # sequence length
    if self.pamCounter > 0:
      self.pamCounter -= 1
    self.learnedSeqLength += 1

    # Phase 1 - turn on the predicted cell in each column that received
    # bottom-up. If there was no predicted cell, pick one to learn to.
    if not self.resetCalled:
      # Uses lrnActiveState['t-1'] and lrnPredictedState['t-1']
      # computes lrnActiveState['t']
      inSequence = self._learnPhase1(activeColumns)

      # Reset our PAM counter if we are in sequence
      if inSequence:
        self.pamCounter = self.pamLength

    # Print status of PAM counter, learned sequence length
    if self.verbosity >= 3:
      print "pamCounter = ", self.pamCounter, "seqLength = ", \
          self.learnedSeqLength

    # Start over on start cells if any of the following occur:
    #  1.) A reset was just called
    #  2.) We have been loo long out of sequence (the pamCounter has expired)
    #  3.) We have reached maximum allowed sequence length.
    #
    # Note that, unless we are following a reset, we also just learned or
    # re-enforced connections to the current set of active columns because
    # this input is still a valid prediction to learn.
    #
    # It is especially helpful to learn the connections to this input when
    # you have a maxSeqLength constraint in place. Otherwise, you will have
    # no continuity at all between sub-sequences of length maxSeqLength.
    if (self.resetCalled or self.pamCounter == 0 or
        (self.maxSeqLength != 0 and
         self.learnedSeqLength >= self.maxSeqLength)):
      if  self.verbosity >= 3:
        if self.resetCalled:
          print "Starting over:", activeColumns, "(reset was called)"
        elif self.pamCounter == 0:
          print "Starting over:", activeColumns, "(PAM counter expired)"
        else:
          print "Starting over:", activeColumns, "(reached maxSeqLength)"

      # Update average learned sequence length - this is a diagnostic statistic
      if self.pamCounter == 0:
        seqLength = self.learnedSeqLength - self.pamLength
      else:
        seqLength = self.learnedSeqLength
      if  self.verbosity >= 3:
        print "  learned sequence length was:", seqLength
      self._updateAvgLearnedSeqLength(seqLength)

      # Backtrack to an earlier starting point, if we find one
      backSteps = 0
      if not self.resetCalled:
        backSteps = self._learnBacktrack()

      # Start over in the current time step if reset was called, or we couldn't
      # backtrack.
      if self.resetCalled or backSteps is None or backSteps == 0:
        backSteps = 0
        self.lrnActiveState['t'].fill(0)
        for c in activeColumns:
          self.lrnActiveState['t'][c, 0] = 1

        # Remove any old input history patterns
        self._prevLrnPatterns = []

      # Reset PAM counter
      self.pamCounter =  self.pamLength
      self.learnedSeqLength = backSteps

      # Clear out any old segment updates from prior sequences
      self.segmentUpdates = {}

    # Phase 2 - Compute new predicted state. When computing predictions for
    # phase 2, we predict at  most one cell per column (the one with the best
    # matching segment).
    self._learnPhase2()