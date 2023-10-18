def _addResults(self, results):
    """
    Stores the current model results in the manager's internal store

    Parameters:
    -----------------------------------------------------------------------
    results:  A ModelResults object that contains the current timestep's
              input/inferences
    """
    # -----------------------------------------------------------------------
    # If the model potentially has temporal inferences.
    if self.__isTemporal:
      shiftedInferences = self.__inferenceShifter.shift(results).inferences
      self.__currentResult = copy.deepcopy(results)
      self.__currentResult.inferences = shiftedInferences
      self.__currentInference = shiftedInferences

    # -----------------------------------------------------------------------
    # The current model has no temporal inferences.
    else:
      self.__currentResult = copy.deepcopy(results)
      self.__currentInference = copy.deepcopy(results.inferences)

    # -----------------------------------------------------------------------
    # Save the current ground-truth results
    self.__currentGroundTruth = copy.deepcopy(results)