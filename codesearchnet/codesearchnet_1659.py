def write(self, proto):
    """Populate serialization proto instance.

    :param proto: (BacktrackingTMProto) the proto instance to populate
    """
    proto.version = TM_VERSION
    self._random.write(proto.random)
    proto.numberOfCols = self.numberOfCols
    proto.cellsPerColumn = self.cellsPerColumn
    proto.initialPerm = float(self.initialPerm)
    proto.connectedPerm = float(self.connectedPerm)
    proto.minThreshold = self.minThreshold
    proto.newSynapseCount = self.newSynapseCount
    proto.permanenceInc = float(self.permanenceInc)
    proto.permanenceDec = float(self.permanenceDec)
    proto.permanenceMax = float(self.permanenceMax)
    proto.globalDecay = float(self.globalDecay)
    proto.activationThreshold = self.activationThreshold
    proto.doPooling = self.doPooling
    proto.segUpdateValidDuration = self.segUpdateValidDuration
    proto.burnIn = self.burnIn
    proto.collectStats = self.collectStats
    proto.verbosity = self.verbosity
    proto.pamLength = self.pamLength
    proto.maxAge = self.maxAge
    proto.maxInfBacktrack = self.maxInfBacktrack
    proto.maxLrnBacktrack = self.maxLrnBacktrack
    proto.maxSeqLength = self.maxSeqLength
    proto.maxSegmentsPerCell = self.maxSegmentsPerCell
    proto.maxSynapsesPerSegment = self.maxSynapsesPerSegment
    proto.outputType = self.outputType

    proto.activeColumns = self.activeColumns

    cellListProto = proto.init("cells", len(self.cells))
    for i, columnSegments in enumerate(self.cells):
      columnSegmentsProto = cellListProto.init(i, len(columnSegments))
      for j, cellSegments in enumerate(columnSegments):
        cellSegmentsProto = columnSegmentsProto.init(j, len(cellSegments))
        for k, segment in enumerate(cellSegments):
          segment.write(cellSegmentsProto[k])

    proto.lrnIterationIdx = self.lrnIterationIdx
    proto.iterationIdx = self.iterationIdx
    proto.segID = self.segID
    if self.currentOutput is None:
      proto.currentOutput.none = None
    else:
      proto.currentOutput.list = self.currentOutput.tolist()
    proto.pamCounter = self.pamCounter
    proto.collectSequenceStats = self.collectSequenceStats
    proto.resetCalled = self.resetCalled
    # In case of None, use negative value as placeholder for serialization
    proto.avgInputDensity = self.avgInputDensity or -1.0
    proto.learnedSeqLength = self.learnedSeqLength
    proto.avgLearnedSeqLength = self.avgLearnedSeqLength

    proto.prevLrnPatterns = self._prevLrnPatterns
    proto.prevInfPatterns = self._prevInfPatterns

    segmentUpdatesListProto = proto.init("segmentUpdates",
                                         len(self.segmentUpdates))
    for i, (key, updates) in enumerate(self.segmentUpdates.iteritems()):
      cellSegmentUpdatesProto = segmentUpdatesListProto[i]
      cellSegmentUpdatesProto.columnIdx = key[0]
      cellSegmentUpdatesProto.cellIdx = key[1]
      segmentUpdatesProto = cellSegmentUpdatesProto.init("segmentUpdates",
                                                         len(updates))
      for j, (lrnIterationIdx, segmentUpdate) in enumerate(updates):
        segmentUpdateWrapperProto = segmentUpdatesProto[j]
        segmentUpdateWrapperProto.lrnIterationIdx = lrnIterationIdx
        segmentUpdate.write(segmentUpdateWrapperProto.segmentUpdate)

    # self.cellConfidence
    proto.cellConfidenceT = self.cellConfidence["t"].tolist()
    proto.cellConfidenceT1 = self.cellConfidence["t-1"].tolist()
    proto.cellConfidenceCandidate = self.cellConfidence["candidate"].tolist()

    # self.colConfidence
    proto.colConfidenceT = self.colConfidence["t"].tolist()
    proto.colConfidenceT1 = self.colConfidence["t-1"].tolist()
    proto.colConfidenceCandidate = self.colConfidence["candidate"].tolist()

    # self.lrnActiveState
    proto.lrnActiveStateT = self.lrnActiveState["t"].tolist()
    proto.lrnActiveStateT1 = self.lrnActiveState["t-1"].tolist()

    # self.infActiveState
    proto.infActiveStateT = self.infActiveState["t"].tolist()
    proto.infActiveStateT1 = self.infActiveState["t-1"].tolist()
    proto.infActiveStateBackup = self.infActiveState["backup"].tolist()
    proto.infActiveStateCandidate = self.infActiveState["candidate"].tolist()

    # self.lrnPredictedState
    proto.lrnPredictedStateT = self.lrnPredictedState["t"].tolist()
    proto.lrnPredictedStateT1 = self.lrnPredictedState["t-1"].tolist()

    # self.infPredictedState
    proto.infPredictedStateT = self.infPredictedState["t"].tolist()
    proto.infPredictedStateT1 = self.infPredictedState["t-1"].tolist()
    proto.infPredictedStateBackup = self.infPredictedState["backup"].tolist()
    proto.infPredictedStateCandidate = self.infPredictedState["candidate"].tolist()

    proto.consolePrinterVerbosity = self.consolePrinterVerbosity