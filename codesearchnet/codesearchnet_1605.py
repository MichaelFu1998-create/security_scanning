def compute(self, bottomUpInput, enableLearn, enableInference=None):
    """
    Overrides :meth:`nupic.algorithms.backtracking_tm.BacktrackingTM.compute`.
    """
    # The C++ TM takes 32 bit floats as input. uint32 works as well since the
    # code only checks whether elements are non-zero
    assert (bottomUpInput.dtype == numpy.dtype('float32')) or \
           (bottomUpInput.dtype == numpy.dtype('uint32')) or \
           (bottomUpInput.dtype == numpy.dtype('int32'))

    self.iterationIdx = self.iterationIdx + 1

    # As a speed optimization for now (until we need online learning), skip
    #  computing the inference output while learning
    if enableInference is None:
      if enableLearn:
        enableInference = False
      else:
        enableInference = True

    # ====================================================================
    # Run compute and retrieve selected state and member variables
    self._setStatePointers()
    y = self.cells4.compute(bottomUpInput, enableInference, enableLearn)
    self.currentOutput = y.reshape((self.numberOfCols, self.cellsPerColumn))
    self.avgLearnedSeqLength = self.cells4.getAvgLearnedSeqLength()
    self._copyAllocatedStates()


    # ========================================================================
    # Update the prediction score stats
    # Learning always includes inference
    if self.collectStats:
      activeColumns = bottomUpInput.nonzero()[0]
      if enableInference:
        predictedState = self.infPredictedState['t-1']
      else:
        predictedState = self.lrnPredictedState['t-1']
      self._updateStatsInferEnd(self._internalStats,
                                activeColumns,
                                predictedState,
                                self.colConfidence['t-1'])



    # Finally return the TM output
    output = self._computeOutput()

    # Print diagnostic information based on the current verbosity level
    self.printComputeEnd(output, learn=enableLearn)

    self.resetCalled = False
    return output