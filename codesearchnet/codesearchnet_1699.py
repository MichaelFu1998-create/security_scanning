def _getSegmentActiveSynapses(self, c, i, s, activeState, newSynapses=False):
    """
    Return a segmentUpdate data structure containing a list of proposed
    changes to segment s. Let activeSynapses be the list of active synapses
    where the originating cells have their activeState output = 1 at time step
    t. (This list is empty if s is None since the segment doesn't exist.)
    newSynapses is an optional argument that defaults to false. If newSynapses
    is true, then newSynapseCount - len(activeSynapses) synapses are added to
    activeSynapses. These synapses are randomly chosen from the set of cells
    that have learnState = 1 at timeStep.

    :param c TODO: document
    :param i TODO: document
    :param s TODO: document
    :param activeState TODO: document
    :param newSynapses TODO: document
    """
    activeSynapses = []

    if s is not None: # s can be None, if adding a new segment
      # Here we add *integers* to activeSynapses
      activeSynapses = [idx for idx, syn in enumerate(s.syns) \
                        if activeState[syn[0], syn[1]]]

    if newSynapses: # add a few more synapses

      nSynapsesToAdd = self.newSynapseCount - len(activeSynapses)

      # Here we add *pairs* (colIdx, cellIdx) to activeSynapses
      activeSynapses += self._chooseCellsToLearnFrom(c, i, s, nSynapsesToAdd,
                                                     activeState)

    # It's still possible that activeSynapses is empty, and this will
    # be handled in addToSegmentUpdates

    # NOTE: activeSynapses contains a mixture of integers and pairs of integers
    # - integers are indices of synapses already existing on the segment,
    #   that we will need to update.
    # - pairs represent source (colIdx, cellIdx) of new synapses to create on
    #   the segment
    update = BacktrackingTM._SegmentUpdate(c, i, s, activeSynapses)

    return update