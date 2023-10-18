def _initEphemerals(self):
    """
    Initialize all ephemeral members after being restored to a pickled state.
    """
    ## We store the lists of segments updates, per cell, so that they can be
    # applied later during learning, when the cell gets bottom-up activation.
    # We store one list per cell. The lists are identified with a hash key which
    # is a tuple (column index, cell index).
    self.segmentUpdates = {}

    # Allocate and reset all stats
    self.resetStats()

    # NOTE: We don't use the same backtrack buffer for inference and learning
    # because learning has a different metric for determining if an input from
    # the past is potentially useful again for backtracking.
    #
    # Our inference backtrack buffer. This keeps track of up to
    # maxInfBacktrack of previous input. Each entry is a list of active column
    # inputs.
    self._prevInfPatterns = []

    # Our learning backtrack buffer. This keeps track of up to maxLrnBacktrack
    # of previous input. Each entry is a list of active column inputs
    self._prevLrnPatterns = []

    # Keep integers rather than bools. Float?
    stateShape = (self.numberOfCols, self.cellsPerColumn)

    self.lrnActiveState = {}
    self.lrnActiveState["t"] = numpy.zeros(stateShape, dtype="int8")
    self.lrnActiveState["t-1"] = numpy.zeros(stateShape, dtype="int8")

    self.lrnPredictedState = {}
    self.lrnPredictedState["t"] = numpy.zeros(stateShape, dtype="int8")
    self.lrnPredictedState["t-1"] = numpy.zeros(stateShape, dtype="int8")

    self.infActiveState = {}
    self.infActiveState["t"] = numpy.zeros(stateShape, dtype="int8")
    self.infActiveState["t-1"] = numpy.zeros(stateShape, dtype="int8")
    self.infActiveState["backup"] = numpy.zeros(stateShape, dtype="int8")
    self.infActiveState["candidate"] = numpy.zeros(stateShape, dtype="int8")

    self.infPredictedState = {}
    self.infPredictedState["t"] = numpy.zeros(stateShape, dtype="int8")
    self.infPredictedState["t-1"] = numpy.zeros(stateShape, dtype="int8")
    self.infPredictedState["backup"] = numpy.zeros(stateShape, dtype="int8")
    self.infPredictedState["candidate"] = numpy.zeros(stateShape, dtype="int8")

    self.cellConfidence = {}
    self.cellConfidence["t"] = numpy.zeros(stateShape, dtype="float32")
    self.cellConfidence["t-1"] = numpy.zeros(stateShape, dtype="float32")
    self.cellConfidence["candidate"] = numpy.zeros(stateShape, dtype="float32")

    self.colConfidence = {}
    self.colConfidence["t"] = numpy.zeros(self.numberOfCols, dtype="float32")
    self.colConfidence["t-1"] = numpy.zeros(self.numberOfCols, dtype="float32")
    self.colConfidence["candidate"] = numpy.zeros(self.numberOfCols,
                                                  dtype="float32")