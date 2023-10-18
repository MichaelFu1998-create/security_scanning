def read(cls, proto):
    """ 
    Reads deserialized data from proto object

    :param proto: (DynamicStructBuilder) Proto object

    :returns: (:class:`Connections`) instance
    """
    #pylint: disable=W0212
    protoCells = proto.cells
    connections = cls(len(protoCells))

    for cellIdx, protoCell in enumerate(protoCells):
      protoCell = protoCells[cellIdx]
      protoSegments = protoCell.segments
      connections._cells[cellIdx] = CellData()
      segments = connections._cells[cellIdx]._segments

      for segmentIdx, protoSegment in enumerate(protoSegments):
        segment = Segment(cellIdx, connections._nextFlatIdx,
                          connections._nextSegmentOrdinal)

        segments.append(segment)
        connections._segmentForFlatIdx.append(segment)
        connections._nextFlatIdx += 1
        connections._nextSegmentOrdinal += 1

        synapses = segment._synapses
        protoSynapses = protoSegment.synapses

        for synapseIdx, protoSynapse in enumerate(protoSynapses):
          presynapticCell = protoSynapse.presynapticCell
          synapse = Synapse(segment, presynapticCell, protoSynapse.permanence,
                            ordinal=connections._nextSynapseOrdinal)
          connections._nextSynapseOrdinal += 1
          synapses.add(synapse)
          connections._synapsesForPresynapticCell[presynapticCell].add(synapse)

          connections._numSynapses += 1

    #pylint: enable=W0212
    return connections