def _growSynapses(cls, connections, random, segment, nDesiredNewSynapes,
                    prevWinnerCells, initialPermanence, maxSynapsesPerSegment):
    """
    Creates nDesiredNewSynapes synapses on the segment passed in if
    possible, choosing random cells from the previous winner cells that are
    not already on the segment.

    :param connections:        (Object) Connections instance for the tm
    :param random:             (Object) TM object used to generate random
                                        numbers
    :param segment:            (int)    Segment to grow synapses on.
    :param nDesiredNewSynapes: (int)    Desired number of synapses to grow
    :param prevWinnerCells:    (list)   Winner cells in `t-1`
    :param initialPermanence:  (float)  Initial permanence of a new synapse.

    """
    candidates = list(prevWinnerCells)

    for synapse in connections.synapsesForSegment(segment):
      i = binSearch(candidates, synapse.presynapticCell)
      if i != -1:
        del candidates[i]

    nActual = min(nDesiredNewSynapes, len(candidates))

    # Check if we're going to surpass the maximum number of synapses.
    overrun = connections.numSynapses(segment) + nActual - maxSynapsesPerSegment
    if overrun > 0:
      cls._destroyMinPermanenceSynapses(connections, random, segment, overrun,
                                        prevWinnerCells)

    # Recalculate in case we weren't able to destroy as many synapses as needed.
    nActual = min(nActual,
                  maxSynapsesPerSegment - connections.numSynapses(segment))

    for _ in range(nActual):
      i = random.getUInt32(len(candidates))
      connections.createSynapse(segment, candidates[i], initialPermanence)
      del candidates[i]