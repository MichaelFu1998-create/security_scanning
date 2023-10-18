def read(cls, proto):
    """
    Reads deserialized data from proto object.

    :param proto: (DynamicStructBuilder) Proto object

    :returns: (:class:TemporalMemory) TemporalMemory instance
    """
    tm = object.__new__(cls)

    # capnp fails to save a tuple, so proto.columnDimensions was forced to
    # serialize as a list.  We prefer a tuple, however, because columnDimensions
    # should be regarded as immutable.
    tm.columnDimensions = tuple(proto.columnDimensions)
    tm.cellsPerColumn = int(proto.cellsPerColumn)
    tm.activationThreshold = int(proto.activationThreshold)
    tm.initialPermanence = round(proto.initialPermanence, EPSILON_ROUND)
    tm.connectedPermanence = round(proto.connectedPermanence, EPSILON_ROUND)
    tm.minThreshold = int(proto.minThreshold)
    tm.maxNewSynapseCount = int(proto.maxNewSynapseCount)
    tm.permanenceIncrement = round(proto.permanenceIncrement, EPSILON_ROUND)
    tm.permanenceDecrement = round(proto.permanenceDecrement, EPSILON_ROUND)
    tm.predictedSegmentDecrement = round(proto.predictedSegmentDecrement,
                                         EPSILON_ROUND)

    tm.maxSegmentsPerCell = int(proto.maxSegmentsPerCell)
    tm.maxSynapsesPerSegment = int(proto.maxSynapsesPerSegment)

    tm.connections = Connections.read(proto.connections)
    #pylint: disable=W0212
    tm._random = Random()
    tm._random.read(proto.random)
    #pylint: enable=W0212

    tm.activeCells = [int(x) for x in proto.activeCells]
    tm.winnerCells = [int(x) for x in proto.winnerCells]

    flatListLength = tm.connections.segmentFlatListLength()
    tm.numActiveConnectedSynapsesForSegment = [0] * flatListLength
    tm.numActivePotentialSynapsesForSegment = [0] * flatListLength
    tm.lastUsedIterationForSegment = [0] * flatListLength

    tm.activeSegments = []
    tm.matchingSegments = []

    for protoSegment in proto.activeSegments:
      tm.activeSegments.append(
        tm.connections.getSegment(protoSegment.cell,
                                  protoSegment.idxOnCell))

    for protoSegment in proto.matchingSegments:
      tm.matchingSegments.append(
        tm.connections.getSegment(protoSegment.cell,
                                  protoSegment.idxOnCell))

    for protoSegment in proto.numActivePotentialSynapsesForSegment:
      segment = tm.connections.getSegment(protoSegment.cell,
                                          protoSegment.idxOnCell)

      tm.numActivePotentialSynapsesForSegment[segment.flatIdx] = (
        int(protoSegment.number))

    tm.iteration = long(proto.iteration)

    for protoSegment in proto.lastUsedIterationForSegment:
      segment = tm.connections.getSegment(protoSegment.cell,
                                          protoSegment.idxOnCell)

      tm.lastUsedIterationForSegment[segment.flatIdx] = (
        long(protoSegment.number))

    return tm