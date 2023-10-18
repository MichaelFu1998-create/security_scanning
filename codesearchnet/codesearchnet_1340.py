def compute(self, bottomUpInput, enableLearn, computeInfOutput=None):
    """
    (From `backtracking_tm.py`)
    Handle one compute, possibly learning.

    @param bottomUpInput     The bottom-up input, typically from a spatial pooler
    @param enableLearn       If true, perform learning
    @param computeInfOutput  If None, default behavior is to disable the inference
                             output when enableLearn is on.
                             If true, compute the inference output
                             If false, do not compute the inference output
    """
    super(MonitoredTMShim, self).compute(set(bottomUpInput.nonzero()[0]),
                                         learn=enableLearn)
    numberOfCells = self.numberOfCells()

    activeState = numpy.zeros(numberOfCells)
    activeState[self.getActiveCells()] = 1
    self.infActiveState["t"] = activeState

    output = numpy.zeros(numberOfCells)
    output[self.getPredictiveCells() + self.getActiveCells()] = 1
    return output