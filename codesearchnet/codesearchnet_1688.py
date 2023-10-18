def _learnPhase2(self, readOnly=False):
    """
    Compute the predicted segments given the current set of active cells.

    :param readOnly       True if being called from backtracking logic.
                          This tells us not to increment any segment
                          duty cycles or queue up any updates.

    This computes the lrnPredictedState['t'] and queues up any segments that
    became active (and the list of active synapses for each segment) into
    the segmentUpdates queue

    This looks at:
        - @ref lrnActiveState['t']

    This modifies:
        - @ref lrnPredictedState['t']
        - @ref segmentUpdates
    """
    # Clear out predicted state to start with
    self.lrnPredictedState['t'].fill(0)

    # Compute new predicted state. When computing predictions for
    # phase 2, we predict at  most one cell per column (the one with the best
    # matching segment).
    for c in xrange(self.numberOfCols):

      # Is there a cell predicted to turn on in this column?
      i, s, numActive = self._getBestMatchingCell(
          c, self.lrnActiveState['t'], minThreshold = self.activationThreshold)
      if i is None:
        continue

      # Turn on the predicted state for the best matching cell and queue
      #  the pertinent segment up for an update, which will get processed if
      #  the cell receives bottom up in the future.
      self.lrnPredictedState['t'][c, i] = 1
      if readOnly:
        continue

      # Queue up this segment for updating
      segUpdate = self._getSegmentActiveSynapses(
          c, i, s, activeState=self.lrnActiveState['t'],
          newSynapses=(numActive < self.newSynapseCount))

      s.totalActivations += 1    # increment totalActivations
      self._addToSegmentUpdates(c, i, segUpdate)

      if self.doPooling:
        # creates a new pooling segment if no best matching segment found
        # sum(all synapses) >= minThreshold, "weak" activation
        predSegment = self._getBestMatchingSegment(c, i,
                                                   self.lrnActiveState['t-1'])
        segUpdate = self._getSegmentActiveSynapses(c, i, predSegment,
                                                   self.lrnActiveState['t-1'], newSynapses=True)
        self._addToSegmentUpdates(c, i, segUpdate)