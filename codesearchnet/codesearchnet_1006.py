def computeActivity(self, activePresynapticCells, connectedPermanence):
    """ 
    Compute each segment's number of active synapses for a given input.
    In the returned lists, a segment's active synapse count is stored at index
    ``segment.flatIdx``.

    :param activePresynapticCells: (iter) Active cells.
    :param connectedPermanence: (float) Permanence threshold for a synapse to be 
           considered connected

    :returns: (tuple) (``numActiveConnectedSynapsesForSegment`` [list],
                      ``numActivePotentialSynapsesForSegment`` [list])
    """

    numActiveConnectedSynapsesForSegment = [0] * self._nextFlatIdx
    numActivePotentialSynapsesForSegment = [0] * self._nextFlatIdx

    threshold = connectedPermanence - EPSILON

    for cell in activePresynapticCells:
      for synapse in self._synapsesForPresynapticCell[cell]:
        flatIdx = synapse.segment.flatIdx
        numActivePotentialSynapsesForSegment[flatIdx] += 1
        if synapse.permanence > threshold:
          numActiveConnectedSynapsesForSegment[flatIdx] += 1

    return (numActiveConnectedSynapsesForSegment,
            numActivePotentialSynapsesForSegment)