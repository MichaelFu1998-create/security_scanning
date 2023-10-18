def activateDendrites(self, learn=True):
    """
    Calculate dendrite segment activity, using the current active cells.

    :param learn: (bool) If true, segment activations will be recorded. This 
           information is used during segment cleanup.

    **Pseudocode:**
    
    ::

      for each distal dendrite segment with activity >= activationThreshold
        mark the segment as active
      for each distal dendrite segment with unconnected activity >= minThreshold
        mark the segment as matching
    """
    (numActiveConnected,
     numActivePotential) = self.connections.computeActivity(
       self.activeCells,
       self.connectedPermanence)

    activeSegments = (
      self.connections.segmentForFlatIdx(i)
      for i in xrange(len(numActiveConnected))
      if numActiveConnected[i] >= self.activationThreshold
    )

    matchingSegments = (
      self.connections.segmentForFlatIdx(i)
      for i in xrange(len(numActivePotential))
      if numActivePotential[i] >= self.minThreshold
    )

    self.activeSegments = sorted(activeSegments,
                                 key=self.connections.segmentPositionSortKey)
    self.matchingSegments = sorted(matchingSegments,
                                   key=self.connections.segmentPositionSortKey)
    self.numActiveConnectedSynapsesForSegment = numActiveConnected
    self.numActivePotentialSynapsesForSegment = numActivePotential

    if learn:
      for segment in self.activeSegments:
        self.lastUsedIterationForSegment[segment.flatIdx] = self.iteration
      self.iteration += 1