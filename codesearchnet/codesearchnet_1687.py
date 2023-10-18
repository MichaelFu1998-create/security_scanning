def _learnPhase1(self, activeColumns, readOnly=False):
    """
    Compute the learning active state given the predicted state and
    the bottom-up input.

    :param activeColumns list of active bottom-ups
    :param readOnly      True if being called from backtracking logic.
                         This tells us not to increment any segment
                         duty cycles or queue up any updates.
    :returns: True if the current input was sufficiently predicted, OR
             if we started over on startCells. False indicates that the current
             input was NOT predicted, well enough to consider it as "inSequence"

    This looks at:
        - @ref lrnActiveState['t-1']
        - @ref lrnPredictedState['t-1']

    This modifies:
        - @ref lrnActiveState['t']
        - @ref lrnActiveState['t-1']
    """
    # Save previous active state and start out on a clean slate
    self.lrnActiveState['t'].fill(0)

    # For each column, turn on the predicted cell. There will always be at most
    # one predicted cell per column
    numUnpredictedColumns = 0
    for c in activeColumns:
      predictingCells = numpy.where(self.lrnPredictedState['t-1'][c] == 1)[0]
      numPredictedCells = len(predictingCells)
      assert numPredictedCells <= 1

      # If we have a predicted cell, turn it on. The segment's posActivation
      # count will have already been incremented by processSegmentUpdates
      if numPredictedCells == 1:
        i = predictingCells[0]
        self.lrnActiveState['t'][c, i] = 1
        continue

      numUnpredictedColumns += 1
      if readOnly:
        continue

      # If no predicted cell, pick the closest matching one to reinforce, or
      # if none exists, create a new segment on a cell in that column
      i, s, numActive = self._getBestMatchingCell(
          c, self.lrnActiveState['t-1'], self.minThreshold)
      if s is not None and s.isSequenceSegment():
        if self.verbosity >= 4:
          print "Learn branch 0, found segment match. Learning on col=", c
        self.lrnActiveState['t'][c, i] = 1
        segUpdate = self._getSegmentActiveSynapses(
            c, i, s, self.lrnActiveState['t-1'], newSynapses = True)
        s.totalActivations += 1
        # This will update the permanences, posActivationsCount, and the
        # lastActiveIteration (age).
        trimSegment = self._adaptSegment(segUpdate)
        if trimSegment:
          self._trimSegmentsInCell(c, i, [s], minPermanence = 0.00001,
                                   minNumSyns = 0)

      # If no close match exists, create a new one
      else:
        # Choose a cell in this column to add a new segment to
        i = self._getCellForNewSegment(c)
        if (self.verbosity >= 4):
          print "Learn branch 1, no match. Learning on col=", c,
          print ", newCellIdxInCol=", i
        self.lrnActiveState['t'][c, i] = 1
        segUpdate = self._getSegmentActiveSynapses(
            c, i, None, self.lrnActiveState['t-1'], newSynapses=True)
        segUpdate.sequenceSegment = True # Make it a sequence segment
        self._adaptSegment(segUpdate)  # No need to check whether perm reached 0

    # Determine if we are out of sequence or not and reset our PAM counter
    # if we are in sequence
    numBottomUpColumns = len(activeColumns)
    if numUnpredictedColumns < numBottomUpColumns / 2:
      return True   # in sequence
    else:
      return False