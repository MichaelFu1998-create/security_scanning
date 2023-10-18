def createSynapse(self, segment, presynapticCell, permanence):
    """ 
    Creates a new synapse on a segment.

    :param segment: (:class:`Segment`) Segment object for synapse to be synapsed 
           to.
    :param presynapticCell: (int) Source cell index.
    :param permanence: (float) Initial permanence of synapse.
    :returns: (:class:`Synapse`) created synapse
    """
    idx = len(segment._synapses)
    synapse = Synapse(segment, presynapticCell, permanence,
                      self._nextSynapseOrdinal)
    self._nextSynapseOrdinal += 1
    segment._synapses.add(synapse)

    self._synapsesForPresynapticCell[presynapticCell].add(synapse)

    self._numSynapses += 1

    return synapse