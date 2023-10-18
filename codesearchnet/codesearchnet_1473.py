def _destroyMinPermanenceSynapses(cls, connections, random, segment,
                                    nDestroy, excludeCells):
    """
    Destroy nDestroy synapses on the specified segment, but don't destroy
    synapses to the "excludeCells".
    """

    destroyCandidates = sorted(
      (synapse for synapse in connections.synapsesForSegment(segment)
       if synapse.presynapticCell not in excludeCells),
      key=lambda s: s._ordinal
    )

    for _ in xrange(nDestroy):
      if len(destroyCandidates) == 0:
        break

      minSynapse = None
      minPermanence = float("inf")

      for synapse in destroyCandidates:
        if synapse.permanence < minPermanence - EPSILON:
          minSynapse = synapse
          minPermanence = synapse.permanence

      connections.destroySynapse(minSynapse)
      destroyCandidates.remove(minSynapse)