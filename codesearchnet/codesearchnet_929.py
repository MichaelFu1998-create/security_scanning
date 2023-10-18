def _compute(self, inputs, outputs):
    """
    Run one iteration of SPRegion's compute
    """

    #if self.topDownMode and (not 'topDownIn' in inputs):
    #  raise RuntimeError("The input topDownIn must be linked in if "
    #                     "topDownMode is True")

    if self._sfdr is None:
      raise RuntimeError("Spatial pooler has not been initialized")


    if not self.topDownMode:
      #
      # BOTTOM-UP compute
      #

      self._iterations += 1

      # Get our inputs into numpy arrays
      buInputVector = inputs['bottomUpIn']

      resetSignal = False
      if 'resetIn' in inputs:
        assert len(inputs['resetIn']) == 1
        resetSignal = inputs['resetIn'][0] != 0

      # Perform inference and/or learning
      rfOutput = self._doBottomUpCompute(
        rfInput = buInputVector.reshape((1,buInputVector.size)),
        resetSignal = resetSignal
        )

      outputs['bottomUpOut'][:] = rfOutput.flat

    else:
      #
      # TOP-DOWN inference
      #

      topDownIn = inputs.get('topDownIn',None)
      spatialTopDownOut, temporalTopDownOut = self._doTopDownInfer(topDownIn)
      outputs['spatialTopDownOut'][:] = spatialTopDownOut
      if temporalTopDownOut is not None:
        outputs['temporalTopDownOut'][:] = temporalTopDownOut


    # OBSOLETE
    outputs['anomalyScore'][:] = 0