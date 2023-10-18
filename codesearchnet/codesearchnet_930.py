def _doBottomUpCompute(self, rfInput, resetSignal):
    """
    Do one iteration of inference and/or learning and return the result

    Parameters:
    --------------------------------------------
    rfInput:      Input vector. Shape is: (1, inputVectorLen).
    resetSignal:  True if reset is asserted

    """

    # Conditional compute break
    self._conditionalBreak()

    # Save the rfInput for the spInputNonZeros parameter
    self._spatialPoolerInput = rfInput.reshape(-1)
    assert(rfInput.shape[0] == 1)

    # Run inference using the spatial pooler. We learn on the coincidences only
    # if we are in learning mode and trainingStep is set appropriately.

    # Run SFDR bottom-up compute and cache output in self._spatialPoolerOutput

    inputVector = numpy.array(rfInput[0]).astype('uint32')
    outputVector = numpy.zeros(self._sfdr.getNumColumns()).astype('uint32')

    self._sfdr.compute(inputVector, self.learningMode, outputVector)

    self._spatialPoolerOutput[:] = outputVector[:]

    # Direct logging of SP outputs if requested
    if self._fpLogSP:
      output = self._spatialPoolerOutput.reshape(-1)
      outputNZ = output.nonzero()[0]
      outStr = " ".join(["%d" % int(token) for token in outputNZ])
      print >>self._fpLogSP, output.size, outStr

    # Direct logging of SP inputs
    if self._fpLogSPInput:
      output = rfInput.reshape(-1)
      outputNZ = output.nonzero()[0]
      outStr = " ".join(["%d" % int(token) for token in outputNZ])
      print >>self._fpLogSPInput, output.size, outStr

    return self._spatialPoolerOutput