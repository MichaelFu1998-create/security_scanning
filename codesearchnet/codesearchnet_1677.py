def predict(self, nSteps):
    """
    This function gives the future predictions for <nSteps> timesteps starting
    from the current TM state. The TM is returned to its original state at the
    end before returning.

    1. We save the TM state.
    2. Loop for nSteps

       a. Turn-on with lateral support from the current active cells
       b. Set the predicted cells as the next step's active cells. This step
          in learn and infer methods use input here to correct the predictions.
          We don't use any input here.

    3. Revert back the TM state to the time before prediction

    :param nSteps: (int) The number of future time steps to be predicted
    :returns: all the future predictions - a numpy array of type "float32" and
          shape (nSteps, numberOfCols). The ith row gives the tm prediction for 
          each column at a future timestep (t+i+1).
    """
    # Save the TM dynamic state, we will use to revert back in the end
    pristineTPDynamicState = self._getTPDynamicState()

    assert (nSteps>0)

    # multiStepColumnPredictions holds all the future prediction.
    multiStepColumnPredictions = numpy.zeros((nSteps, self.numberOfCols),
                                             dtype="float32")

    # This is a (nSteps-1)+half loop. Phase 2 in both learn and infer methods
    # already predicts for timestep (t+1). We use that prediction for free and
    # save the half-a-loop of work.

    step = 0
    while True:
      # We get the prediction for the columns in the next time step from
      # the topDownCompute method. It internally uses confidences.
      multiStepColumnPredictions[step, :] = self.topDownCompute()

      # Cleanest way in python to handle one and half loops
      if step == nSteps-1:
        break
      step += 1

      # Copy t-1 into t
      self.infActiveState['t-1'][:, :] = self.infActiveState['t'][:, :]
      self.infPredictedState['t-1'][:, :] = self.infPredictedState['t'][:, :]
      self.cellConfidence['t-1'][:, :] = self.cellConfidence['t'][:, :]

      # Predicted state at "t-1" becomes the active state at "t"
      self.infActiveState['t'][:, :] = self.infPredictedState['t-1'][:, :]

      # Predicted state and confidence are set in phase2.
      self.infPredictedState['t'].fill(0)
      self.cellConfidence['t'].fill(0.0)
      self._inferPhase2()

    # Revert the dynamic state to the saved state
    self._setTPDynamicState(pristineTPDynamicState)

    return multiStepColumnPredictions