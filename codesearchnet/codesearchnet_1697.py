def _getBestMatchingSegment(self, c, i, activeState):
    """
    For the given cell, find the segment with the largest number of active
    synapses. This routine is aggressive in finding the best match. The
    permanence value of synapses is allowed to be below connectedPerm. The number
    of active synapses is allowed to be below activationThreshold, but must be
    above minThreshold. The routine returns the segment index. If no segments are
    found, then an index of -1 is returned.

    :param c TODO: document
    :param i TODO: document
    :param activeState TODO: document
    """
    maxActivity, which = self.minThreshold, -1

    for j, s in enumerate(self.cells[c][i]):
      activity = self._getSegmentActivityLevel(s, activeState,
                                               connectedSynapsesOnly=False)

      if activity >= maxActivity:
        maxActivity, which = activity, j

    if which == -1:
      return None
    else:
      return self.cells[c][i][which]