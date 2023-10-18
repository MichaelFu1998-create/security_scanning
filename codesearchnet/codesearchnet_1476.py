def _adaptSegment(cls, connections, segment, prevActiveCells,
                    permanenceIncrement, permanenceDecrement):
    """
    Updates synapses on segment.
    Strengthens active synapses; weakens inactive synapses.

    :param connections:          (Object) Connections instance for the tm
    :param segment:              (int)    Segment to adapt
    :param prevActiveCells:      (list)   Active cells in `t-1`
    :param permanenceIncrement:  (float)  Amount to increment active synapses
    :param permanenceDecrement:  (float)  Amount to decrement inactive synapses
    """

    # Destroying a synapse modifies the set that we're iterating through.
    synapsesToDestroy = []

    for synapse in connections.synapsesForSegment(segment):
      permanence = synapse.permanence

      if binSearch(prevActiveCells, synapse.presynapticCell) != -1:
        permanence += permanenceIncrement
      else:
        permanence -= permanenceDecrement

      # Keep permanence within min/max bounds
      permanence = max(0.0, min(1.0, permanence))

      if permanence < EPSILON:
        synapsesToDestroy.append(synapse)
      else:
        connections.updateSynapsePermanence(synapse, permanence)

    for synapse in synapsesToDestroy:
      connections.destroySynapse(synapse)

    if connections.numSynapses(segment) == 0:
      connections.destroySegment(segment)