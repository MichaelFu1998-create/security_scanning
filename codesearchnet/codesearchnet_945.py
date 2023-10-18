def _compute(self, inputs, outputs):
    """
    Run one iteration of TMRegion's compute
    """

    #if self.topDownMode and (not 'topDownIn' in inputs):
    # raise RuntimeError("The input topDownIn must be linked in if "
    #                    "topDownMode is True")

    if self._tfdr is None:
      raise RuntimeError("TM has not been initialized")

    # Conditional compute break
    self._conditionalBreak()

    self._iterations += 1

    # Get our inputs as numpy array
    buInputVector = inputs['bottomUpIn']

    # Handle reset signal
    resetSignal = False
    if 'resetIn' in inputs:
      assert len(inputs['resetIn']) == 1
      if inputs['resetIn'][0] != 0:
        self._tfdr.reset()
        self._sequencePos = 0  # Position within the current sequence

    if self.computePredictedActiveCellIndices:
      prevPredictedState = self._tfdr.getPredictedState().reshape(-1).astype('float32')

    if self.anomalyMode:
      prevPredictedColumns = self._tfdr.topDownCompute().copy().nonzero()[0]

    # Perform inference and/or learning
    tpOutput = self._tfdr.compute(buInputVector, self.learningMode, self.inferenceMode)
    self._sequencePos += 1

    # OR'ing together the cells in each column?
    if self.orColumnOutputs:
      tpOutput= tpOutput.reshape(self.columnCount,
                                     self.cellsPerColumn).max(axis=1)

    # Direct logging of non-zero TM outputs
    if self._fpLogTPOutput:
      output = tpOutput.reshape(-1)
      outputNZ = tpOutput.nonzero()[0]
      outStr = " ".join(["%d" % int(token) for token in outputNZ])
      print >>self._fpLogTPOutput, output.size, outStr

    # Write the bottom up out to our node outputs
    outputs['bottomUpOut'][:] = tpOutput.flat

    if self.topDownMode:
      # Top-down compute
      outputs['topDownOut'][:] = self._tfdr.topDownCompute().copy()

    # Set output for use with anomaly classification region if in anomalyMode
    if self.anomalyMode:
      activeLearnCells = self._tfdr.getLearnActiveStateT()
      size = activeLearnCells.shape[0] * activeLearnCells.shape[1]
      outputs['lrnActiveStateT'][:] = activeLearnCells.reshape(size)

      activeColumns = buInputVector.nonzero()[0]
      outputs['anomalyScore'][:] = anomaly.computeRawAnomalyScore(
        activeColumns, prevPredictedColumns)

    if self.computePredictedActiveCellIndices:
      # Reshape so we are dealing with 1D arrays
      activeState = self._tfdr._getActiveState().reshape(-1).astype('float32')
      activeIndices = numpy.where(activeState != 0)[0]
      predictedIndices= numpy.where(prevPredictedState != 0)[0]
      predictedActiveIndices = numpy.intersect1d(activeIndices, predictedIndices)
      outputs["activeCells"].fill(0)
      outputs["activeCells"][activeIndices] = 1
      outputs["predictedActiveCells"].fill(0)
      outputs["predictedActiveCells"][predictedActiveIndices] = 1