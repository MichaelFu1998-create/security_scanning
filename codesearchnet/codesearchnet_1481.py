def write(self, proto):
    """
    Writes serialized data to proto object.

    :param proto: (DynamicStructBuilder) Proto object
    """
    # capnp fails to save a tuple.  Let's force columnDimensions to list.
    proto.columnDimensions = list(self.columnDimensions)
    proto.cellsPerColumn = self.cellsPerColumn
    proto.activationThreshold = self.activationThreshold
    proto.initialPermanence = round(self.initialPermanence, EPSILON_ROUND)
    proto.connectedPermanence = round(self.connectedPermanence, EPSILON_ROUND)
    proto.minThreshold = self.minThreshold
    proto.maxNewSynapseCount = self.maxNewSynapseCount
    proto.permanenceIncrement = round(self.permanenceIncrement, EPSILON_ROUND)
    proto.permanenceDecrement = round(self.permanenceDecrement, EPSILON_ROUND)
    proto.predictedSegmentDecrement = self.predictedSegmentDecrement

    proto.maxSegmentsPerCell = self.maxSegmentsPerCell
    proto.maxSynapsesPerSegment = self.maxSynapsesPerSegment

    self.connections.write(proto.connections)
    self._random.write(proto.random)

    proto.activeCells = list(self.activeCells)
    proto.winnerCells = list(self.winnerCells)

    protoActiveSegments = proto.init("activeSegments", len(self.activeSegments))
    for i, segment in enumerate(self.activeSegments):
      protoActiveSegments[i].cell = segment.cell
      idx = self.connections.segmentsForCell(segment.cell).index(segment)
      protoActiveSegments[i].idxOnCell = idx

    protoMatchingSegments = proto.init("matchingSegments",
                                       len(self.matchingSegments))
    for i, segment in enumerate(self.matchingSegments):
      protoMatchingSegments[i].cell = segment.cell
      idx = self.connections.segmentsForCell(segment.cell).index(segment)
      protoMatchingSegments[i].idxOnCell = idx

    protoNumActivePotential = proto.init(
      "numActivePotentialSynapsesForSegment",
      len(self.numActivePotentialSynapsesForSegment))
    for i, numActivePotentialSynapses in enumerate(
        self.numActivePotentialSynapsesForSegment):
      segment = self.connections.segmentForFlatIdx(i)
      if segment is not None:
        protoNumActivePotential[i].cell = segment.cell
        idx = self.connections.segmentsForCell(segment.cell).index(segment)
        protoNumActivePotential[i].idxOnCell = idx
        protoNumActivePotential[i].number = numActivePotentialSynapses

    proto.iteration = self.iteration

    protoLastUsedIteration = proto.init(
      "lastUsedIterationForSegment",
      len(self.numActivePotentialSynapsesForSegment))
    for i, lastUsed in enumerate(self.lastUsedIterationForSegment):
      segment = self.connections.segmentForFlatIdx(i)
      if segment is not None:
        protoLastUsedIteration[i].cell = segment.cell
        idx = self.connections.segmentsForCell(segment.cell).index(segment)
        protoLastUsedIteration[i].idxOnCell = idx
        protoLastUsedIteration[i].number = lastUsed