def _inferBacktrack(self, activeColumns):
    """
    This "backtracks" our inference state, trying to see if we can lock onto
    the current set of inputs by assuming the sequence started up to N steps
    ago on start cells.

    This will adjust @ref infActiveState['t'] if it does manage to lock on to a
    sequence that started earlier. It will also compute infPredictedState['t']
    based on the possibly updated @ref infActiveState['t'], so there is no need to
    call inferPhase2() after calling inferBacktrack().

    This looks at:
        - ``infActiveState['t']``

    This updates/modifies:
        - ``infActiveState['t']``
        - ``infPredictedState['t']``
        - ``colConfidence['t']``
        - ``cellConfidence['t']``

    How it works:

    This method gets called from :meth:`updateInferenceState` when we detect 
    either of the following two conditions:

    #. The current bottom-up input had too many un-expected columns
    #. We fail to generate a sufficient number of predicted columns for the
       next time step.

    Either of these two conditions indicate that we have fallen out of a
    learned sequence.

    Rather than simply "giving up" and bursting on the unexpected input
    columns, a better approach is to see if perhaps we are in a sequence that
    started a few steps ago. The real world analogy is that you are driving
    along and suddenly hit a dead-end, you will typically go back a few turns
    ago and pick up again from a familiar intersection.

    This back-tracking goes hand in hand with our learning methodology, which
    always tries to learn again from start cells after it loses context. This
    results in a network that has learned multiple, overlapping paths through
    the input data, each starting at different points. The lower the global
    decay and the more repeatability in the data, the longer each of these
    paths will end up being.

    The goal of this function is to find out which starting point in the past
    leads to the current input with the most context as possible. This gives us
    the best chance of predicting accurately going forward. Consider the
    following example, where you have learned the following sub-sequences which
    have the given frequencies:

    ::

                  ? - Q - C - D - E      10X      seq 0
                  ? - B - C - D - F      1X       seq 1
                  ? - B - C - H - I      2X       seq 2
                  ? - B - C - D - F      3X       seq 3
          ? - Z - A - B - C - D - J      2X       seq 4
          ? - Z - A - B - C - H - I      1X       seq 5
          ? - Y - A - B - C - D - F      3X       seq 6
  
        ----------------------------------------
      W - X - Z - A - B - C - D          <= input history
                              ^
                              current time step

    Suppose, in the current time step, the input pattern is D and you have not
    predicted D, so you need to backtrack. Suppose we can backtrack up to 6
    steps in the past, which path should we choose? From the table above, we can
    see that the correct answer is to assume we are in seq 4. How do we
    implement the backtrack to give us this right answer? The current
    implementation takes the following approach:

    #. Start from the farthest point in the past.
    #. For each starting point S, calculate the confidence of the current
       input, conf(startingPoint=S), assuming we followed that sequence.
       Note that we must have learned at least one sequence that starts at
       point S.
    #. If conf(startingPoint=S) is significantly different from
       conf(startingPoint=S-1), then choose S-1 as the starting point.

    The assumption here is that starting point S-1 is the starting point of
    a learned sub-sequence that includes the current input in it's path and
    that started the longest ago. It thus has the most context and will be
    the best predictor going forward.

    From the statistics in the above table, we can compute what the confidences
    will be for each possible starting point:

    ::
  
      startingPoint           confidence of D
      -----------------------------------------
      B (t-2)               4/6  = 0.667   (seq 1,3)/(seq 1,2,3)
      Z (t-4)               2/3  = 0.667   (seq 4)/(seq 4,5)

    First of all, we do not compute any confidences at starting points t-1, t-3,
    t-5, t-6 because there are no learned sequences that start at those points.

    Notice here that Z is the starting point of the longest sub-sequence leading
    up to the current input. Event though starting at t-2 and starting at t-4
    give the same confidence value, we choose the sequence starting at t-4
    because it gives the most context, and it mirrors the way that learning
    extends sequences.

    :param activeColumns: (list) of active column indices

    """
    # How much input history have we accumulated?
    # The current input is always at the end of self._prevInfPatterns (at
    # index -1), but it is also evaluated as a potential starting point by
    # turning on it's start cells and seeing if it generates sufficient
    # predictions going forward.
    numPrevPatterns = len(self._prevInfPatterns)
    if numPrevPatterns <= 0:
      return

    # This is an easy to use label for the current time step
    currentTimeStepsOffset = numPrevPatterns - 1

    # Save our current active state in case we fail to find a place to restart
    # todo: save infActiveState['t-1'], infPredictedState['t-1']?
    self.infActiveState['backup'][:, :] = self.infActiveState['t'][:, :]

    # Save our t-1 predicted state because we will write over it as as evaluate
    # each potential starting point.
    self.infPredictedState['backup'][:, :] = self.infPredictedState['t-1'][:, :]

    # We will record which previous input patterns did not generate predictions
    # up to the current time step and remove all the ones at the head of the
    # input history queue so that we don't waste time evaluating them again at
    # a later time step.
    badPatterns = []

    # Let's go back in time and replay the recent inputs from start cells and
    #  see if we can lock onto this current set of inputs that way.
    #
    # Start the farthest back and work our way forward. For each starting point,
    #  See if firing on start cells at that point would predict the current
    #  input as well as generate sufficient predictions for the next time step.
    #
    # We want to pick the point closest to the current time step that gives us
    # the relevant confidence. Think of this example, where we are at D and need
    # to
    #   A - B - C - D
    # decide if we should backtrack to C, B, or A. Suppose B-C-D is a high order
    # sequence and A is unrelated to it. If we backtrock to B would we get a
    # certain confidence of D, but if went went farther back, to A, the
    # confidence wouldn't change, since A has no impact on the B-C-D series.
    #
    # So, our strategy will be to pick the "B" point, since choosing the A point
    #  does not impact our confidences going forward at all.
    inSequence = False
    candConfidence = None
    candStartOffset = None
    for startOffset in range(0, numPrevPatterns):

      # If we have a candidate already in the past, don't bother falling back
      #  to start cells on the current input.
      if startOffset == currentTimeStepsOffset and candConfidence is not None:
        break

      if self.verbosity >= 3:
        print (
            "Trying to lock-on using startCell state from %d steps ago:" % (
                numPrevPatterns - 1 - startOffset),
            self._prevInfPatterns[startOffset])

      # Play through starting from starting point 'startOffset'
      inSequence = False
      for offset in range(startOffset, numPrevPatterns):
        # If we are about to set the active columns for the current time step
        # based on what we predicted, capture and save the total confidence of
        # predicting the current input
        if offset == currentTimeStepsOffset:
          totalConfidence = self.colConfidence['t'][activeColumns].sum()

        # Compute activeState[t] given bottom-up and predictedState[t-1]
        self.infPredictedState['t-1'][:, :] = self.infPredictedState['t'][:, :]
        inSequence = self._inferPhase1(self._prevInfPatterns[offset],
                                       useStartCells = (offset == startOffset))
        if not inSequence:
          break

        # Compute predictedState['t'] given activeState['t']
        if self.verbosity >= 3:
          print ("  backtrack: computing predictions from ",
                 self._prevInfPatterns[offset])
        inSequence = self._inferPhase2()
        if not inSequence:
          break

      # If starting from startOffset got lost along the way, mark it as an
      # invalid start point.
      if not inSequence:
        badPatterns.append(startOffset)
        continue

      # If we got to here, startOffset is a candidate starting point.
      # Save this state as a candidate state. It will become the chosen state if
      # we detect a change in confidences starting at a later startOffset
      candConfidence = totalConfidence
      candStartOffset = startOffset

      if self.verbosity >= 3 and startOffset != currentTimeStepsOffset:
        print ("  # Prediction confidence of current input after starting %d "
               "steps ago:" % (numPrevPatterns - 1 - startOffset),
               totalConfidence)

      if candStartOffset == currentTimeStepsOffset:  # no more to try
        break
      self.infActiveState['candidate'][:, :] = self.infActiveState['t'][:, :]
      self.infPredictedState['candidate'][:, :] = (
          self.infPredictedState['t'][:, :])
      self.cellConfidence['candidate'][:, :] = self.cellConfidence['t'][:, :]
      self.colConfidence['candidate'][:] = self.colConfidence['t'][:]
      break

    # If we failed to lock on at any starting point, fall back to the original
    # active state that we had on entry
    if candStartOffset is None:
      if self.verbosity >= 3:
        print "Failed to lock on. Falling back to bursting all unpredicted."
      self.infActiveState['t'][:, :] = self.infActiveState['backup'][:, :]
      self._inferPhase2()

    else:
      if self.verbosity >= 3:
        print ("Locked on to current input by using start cells from %d "
               " steps ago:" % (numPrevPatterns - 1 - candStartOffset),
               self._prevInfPatterns[candStartOffset])
      # Install the candidate state, if it wasn't the last one we evaluated.
      if candStartOffset != currentTimeStepsOffset:
        self.infActiveState['t'][:, :] = self.infActiveState['candidate'][:, :]
        self.infPredictedState['t'][:, :] = (
            self.infPredictedState['candidate'][:, :])
        self.cellConfidence['t'][:, :] = self.cellConfidence['candidate'][:, :]
        self.colConfidence['t'][:] = self.colConfidence['candidate'][:]

    # Remove any useless patterns at the head of the previous input pattern
    # queue.
    for i in range(numPrevPatterns):
      if (i in badPatterns or
          (candStartOffset is not None and i <= candStartOffset)):
        if self.verbosity >= 3:
          print ("Removing useless pattern from history:",
                 self._prevInfPatterns[0])
        self._prevInfPatterns.pop(0)
      else:
        break

    # Restore the original predicted state.
    self.infPredictedState['t-1'][:, :] = self.infPredictedState['backup'][:, :]