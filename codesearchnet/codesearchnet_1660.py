def read(cls, proto):
    """Deserialize from proto instance.

    :param proto: (BacktrackingTMProto) the proto instance to read from
    """
    assert proto.version == TM_VERSION
    obj = object.__new__(cls)
    obj._random = Random()
    obj._random.read(proto.random)
    obj.numberOfCols = int(proto.numberOfCols)
    obj.cellsPerColumn = int(proto.cellsPerColumn)
    obj._numberOfCells = obj.numberOfCols * obj.cellsPerColumn
    obj.initialPerm = numpy.float32(proto.initialPerm)
    obj.connectedPerm = numpy.float32(proto.connectedPerm)
    obj.minThreshold = int(proto.minThreshold)
    obj.newSynapseCount = int(proto.newSynapseCount)
    obj.permanenceInc = numpy.float32(proto.permanenceInc)
    obj.permanenceDec = numpy.float32(proto.permanenceDec)
    obj.permanenceMax = numpy.float32(proto.permanenceMax)
    obj.globalDecay = numpy.float32(proto.globalDecay)
    obj.activationThreshold = int(proto.activationThreshold)
    obj.doPooling = proto.doPooling
    obj.segUpdateValidDuration = int(proto.segUpdateValidDuration)
    obj.burnIn = int(proto.burnIn)
    obj.collectStats = proto.collectStats
    obj.verbosity = int(proto.verbosity)
    obj.pamLength = int(proto.pamLength)
    obj.maxAge = int(proto.maxAge)
    obj.maxInfBacktrack = int(proto.maxInfBacktrack)
    obj.maxLrnBacktrack = int(proto.maxLrnBacktrack)
    obj.maxSeqLength = int(proto.maxSeqLength)
    obj.maxSegmentsPerCell = proto.maxSegmentsPerCell
    obj.maxSynapsesPerSegment = proto.maxSynapsesPerSegment
    obj.outputType = proto.outputType

    obj.activeColumns = [int(col) for col in proto.activeColumns]

    obj.cells = [[] for _ in xrange(len(proto.cells))]
    for columnSegments, columnSegmentsProto in zip(obj.cells, proto.cells):
      columnSegments.extend([[] for _ in xrange(len(columnSegmentsProto))])
      for cellSegments, cellSegmentsProto in zip(columnSegments,
                                                 columnSegmentsProto):
        for segmentProto in cellSegmentsProto:
          segment = Segment.read(segmentProto, obj)
          cellSegments.append(segment)

    obj.lrnIterationIdx = int(proto.lrnIterationIdx)
    obj.iterationIdx = int(proto.iterationIdx)
    obj.segID = int(proto.segID)

    obj.pamCounter = int(proto.pamCounter)
    obj.collectSequenceStats = proto.collectSequenceStats
    obj.resetCalled = proto.resetCalled
    avgInputDensity = proto.avgInputDensity
    if avgInputDensity < 0.0:
      # Negative value placeholder indicates None
      obj.avgInputDensity = None
    else:
      obj.avgInputDensity = avgInputDensity
    obj.learnedSeqLength = int(proto.learnedSeqLength)
    obj.avgLearnedSeqLength = proto.avgLearnedSeqLength

    # Initialize various structures
    obj._initEphemerals()

    if proto.currentOutput.which() == "none":
      obj.currentOutput = None
    else:
      obj.currentOutput = numpy.array(proto.currentOutput.list,
                                      dtype='float32')

    for pattern in proto.prevLrnPatterns:
      obj.prevLrnPatterns.append([v for v in pattern])
    for pattern in proto.prevInfPatterns:
      obj.prevInfPatterns.append([v for v in pattern])

    for cellWrapperProto in proto.segmentUpdates:
      key = (cellWrapperProto.columnIdx, cellWrapperProto.cellIdx)
      value = []
      for updateWrapperProto in cellWrapperProto.segmentUpdates:
        segmentUpdate = SegmentUpdate.read(updateWrapperProto.segmentUpdate, obj)
        value.append((int(updateWrapperProto.lrnIterationIdx), segmentUpdate))
      obj.segmentUpdates[key] = value

    # cellConfidence
    numpy.copyto(obj.cellConfidence["t"], proto.cellConfidenceT)
    numpy.copyto(obj.cellConfidence["t-1"], proto.cellConfidenceT1)
    numpy.copyto(obj.cellConfidence["candidate"],
                 proto.cellConfidenceCandidate)

    # colConfidence
    numpy.copyto(obj.colConfidence["t"], proto.colConfidenceT)
    numpy.copyto(obj.colConfidence["t-1"], proto.colConfidenceT1)
    numpy.copyto(obj.colConfidence["candidate"], proto.colConfidenceCandidate)

    # lrnActiveState
    numpy.copyto(obj.lrnActiveState["t"], proto.lrnActiveStateT)
    numpy.copyto(obj.lrnActiveState["t-1"], proto.lrnActiveStateT1)

    # infActiveState
    numpy.copyto(obj.infActiveState["t"], proto.infActiveStateT)
    numpy.copyto(obj.infActiveState["t-1"], proto.infActiveStateT1)
    numpy.copyto(obj.infActiveState["backup"], proto.infActiveStateBackup)
    numpy.copyto(obj.infActiveState["candidate"],
                 proto.infActiveStateCandidate)

    # lrnPredictedState
    numpy.copyto(obj.lrnPredictedState["t"], proto.lrnPredictedStateT)
    numpy.copyto(obj.lrnPredictedState["t-1"], proto.lrnPredictedStateT1)

    # infPredictedState
    numpy.copyto(obj.infPredictedState["t"], proto.infPredictedStateT)
    numpy.copyto(obj.infPredictedState["t-1"], proto.infPredictedStateT1)
    numpy.copyto(obj.infPredictedState["backup"],
                 proto.infPredictedStateBackup)
    numpy.copyto(obj.infPredictedState["candidate"],
                 proto.infPredictedStateCandidate)

    obj.consolePrinterVerbosity = int(proto.consolePrinterVerbosity)

    return obj