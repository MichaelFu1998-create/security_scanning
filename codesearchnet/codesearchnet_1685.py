def _learnBacktrackFrom(self, startOffset, readOnly=True):
    """
    A utility method called from learnBacktrack. This will backtrack
    starting from the given startOffset in our prevLrnPatterns queue.

    It returns True if the backtrack was successful and we managed to get
    predictions all the way up to the current time step.

    If readOnly, then no segments are updated or modified, otherwise, all
    segment updates that belong to the given path are applied.
    
    This updates/modifies:

        - lrnActiveState['t']

    This trashes:

        - lrnPredictedState['t']
        - lrnPredictedState['t-1']
        - lrnActiveState['t-1']

    :param startOffset: Start offset within the prevLrnPatterns input history
    :param readOnly: 
    :return: True if we managed to lock on to a sequence that started
                       earlier.
                       If False, we lost predictions somewhere along the way
                       leading up to the current time.
    """
    # How much input history have we accumulated?
    # The current input is always at the end of self._prevInfPatterns (at
    # index -1), but it is also evaluated as a potential starting point by
    # turning on it's start cells and seeing if it generates sufficient
    # predictions going forward.
    numPrevPatterns = len(self._prevLrnPatterns)

    # This is an easy to use label for the current time step
    currentTimeStepsOffset = numPrevPatterns - 1

    # Clear out any old segment updates. learnPhase2() adds to the segment
    # updates if we're not readOnly
    if not readOnly:
      self.segmentUpdates = {}

    # Status message
    if self.verbosity >= 3:
      if readOnly:
        print (
            "Trying to lock-on using startCell state from %d steps ago:" % (
                numPrevPatterns - 1 - startOffset),
            self._prevLrnPatterns[startOffset])
      else:
        print (
            "Locking on using startCell state from %d steps ago:" % (
                numPrevPatterns - 1 - startOffset),
            self._prevLrnPatterns[startOffset])

    # Play through up to the current time step
    inSequence = True
    for offset in range(startOffset, numPrevPatterns):

      # Copy predicted and active states into t-1
      self.lrnPredictedState['t-1'][:, :] = self.lrnPredictedState['t'][:, :]
      self.lrnActiveState['t-1'][:, :] = self.lrnActiveState['t'][:, :]

      # Get the input pattern
      inputColumns = self._prevLrnPatterns[offset]

      # Apply segment updates from the last set of predictions
      if not readOnly:
        self._processSegmentUpdates(inputColumns)

      # Phase 1:
      # Compute activeState[t] given bottom-up and predictedState[t-1]
      if offset == startOffset:
        self.lrnActiveState['t'].fill(0)
        for c in inputColumns:
          self.lrnActiveState['t'][c, 0] = 1
        inSequence = True
      else:
        # Uses lrnActiveState['t-1'] and lrnPredictedState['t-1']
        # computes lrnActiveState['t']
        inSequence = self._learnPhase1(inputColumns, readOnly=readOnly)

      # Break out immediately if we fell out of sequence or reached the current
      # time step
      if not inSequence or offset == currentTimeStepsOffset:
        break

      # Phase 2:
      # Computes predictedState['t'] given activeState['t'] and also queues
      # up active segments into self.segmentUpdates, unless this is readOnly
      if self.verbosity >= 3:
        print "  backtrack: computing predictions from ", inputColumns
      self._learnPhase2(readOnly=readOnly)

    # Return whether or not this starting point was valid
    return inSequence