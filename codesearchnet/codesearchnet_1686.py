def _learnBacktrack(self):
    """
    This "backtracks" our learning state, trying to see if we can lock onto
    the current set of inputs by assuming the sequence started up to N steps
    ago on start cells.

    This will adjust @ref lrnActiveState['t'] if it does manage to lock on to a
    sequence that started earlier.

    :returns:          >0 if we managed to lock on to a sequence that started
                      earlier. The value returned is how many steps in the
                      past we locked on.
                      If 0 is returned, the caller needs to change active
                      state to start on start cells.

    How it works:
    -------------------------------------------------------------------
    This method gets called from updateLearningState when we detect either of
    the following two conditions:

    #. Our PAM counter (@ref pamCounter) expired
    #. We reached the max allowed learned sequence length

    Either of these two conditions indicate that we want to start over on start
    cells.

    Rather than start over on start cells on the current input, we can
    accelerate learning by backtracking a few steps ago and seeing if perhaps
    a sequence we already at least partially know already started.

    This updates/modifies:
        - @ref lrnActiveState['t']

    This trashes:
        - @ref lrnActiveState['t-1']
        - @ref lrnPredictedState['t']
        - @ref lrnPredictedState['t-1']

    """
    # How much input history have we accumulated?
    # The current input is always at the end of self._prevInfPatterns (at
    # index -1), and is not a valid startingOffset to evaluate.
    numPrevPatterns = len(self._prevLrnPatterns) - 1
    if numPrevPatterns <= 0:
      if self.verbosity >= 3:
        print "lrnBacktrack: No available history to backtrack from"
      return False

    # We will record which previous input patterns did not generate predictions
    # up to the current time step and remove all the ones at the head of the
    # input history queue so that we don't waste time evaluating them again at
    # a later time step.
    badPatterns = []

    # Let's go back in time and replay the recent inputs from start cells and
    # see if we can lock onto this current set of inputs that way.
    #
    # Start the farthest back and work our way forward. For each starting point,
    # See if firing on start cells at that point would predict the current
    # input.
    #
    # We want to pick the point farthest in the past that has continuity
    # up to the current time step
    inSequence = False
    for startOffset in range(0, numPrevPatterns):
      # Can we backtrack from startOffset?
      inSequence = self._learnBacktrackFrom(startOffset, readOnly=True)

      # Done playing through the sequence from starting point startOffset
      # Break out as soon as we find a good path
      if inSequence:
        break

      # Take this bad starting point out of our input history so we don't
      # try it again later.
      badPatterns.append(startOffset)

    # If we failed to lock on at any starting point, return failure. The caller
    # will start over again on start cells
    if not inSequence:
      if self.verbosity >= 3:
        print ("Failed to lock on. Falling back to start cells on current "
               "time step.")
      # Nothing in our input history was a valid starting point, so get rid
      #  of it so we don't try any of them again at a later iteration
      self._prevLrnPatterns = []
      return False

    # We did find a valid starting point in the past. Now, we need to
    # re-enforce all segments that became active when following this path.
    if self.verbosity >= 3:
      print ("Discovered path to current input by using start cells from %d "
             "steps ago:" % (numPrevPatterns - startOffset),
             self._prevLrnPatterns[startOffset])

    self._learnBacktrackFrom(startOffset, readOnly=False)

    # Remove any useless patterns at the head of the input pattern history
    # queue.
    for i in range(numPrevPatterns):
      if i in badPatterns or i <= startOffset:
        if self.verbosity >= 3:
          print ("Removing useless pattern from history:",
                 self._prevLrnPatterns[0])
        self._prevLrnPatterns.pop(0)
      else:
        break

    return numPrevPatterns - startOffset