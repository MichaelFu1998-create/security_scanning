def compute(self, activeColumns, learn=True):
    """
    Feeds input record through TM, performing inference and learning.
    Updates member variables with new state.

    @param activeColumns (set) Indices of active columns in `t`
    """
    bottomUpInput = numpy.zeros(self.numberOfCols, dtype=dtype)
    bottomUpInput[list(activeColumns)] = 1
    super(TemporalMemoryShim, self).compute(bottomUpInput,
                                            enableLearn=learn,
                                            enableInference=True)

    predictedState = self.getPredictedState()
    self.predictiveCells = set(numpy.flatnonzero(predictedState))