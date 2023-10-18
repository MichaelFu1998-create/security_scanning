def _anomalyCompute(self):
    """
    Compute Anomaly score, if required
    """
    inferenceType = self.getInferenceType()

    inferences = {}
    sp = self._getSPRegion()
    score = None
    if inferenceType == InferenceType.NontemporalAnomaly:
      score = sp.getOutputData("anomalyScore")[0] #TODO move from SP to Anomaly ?

    elif inferenceType == InferenceType.TemporalAnomaly:
      tm = self._getTPRegion()

      if sp is not None:
        activeColumns = sp.getOutputData("bottomUpOut").nonzero()[0]
      else:
        sensor = self._getSensorRegion()
        activeColumns = sensor.getOutputData('dataOut').nonzero()[0]

      if not self._predictedFieldName in self._input:
        raise ValueError(
          "Expected predicted field '%s' in input row, but was not found!"
          % self._predictedFieldName
        )
      # Calculate the anomaly score using the active columns
      # and previous predicted columns.
      score = tm.getOutputData("anomalyScore")[0]

      # Calculate the classifier's output and use the result as the anomaly
      # label. Stores as string of results.

      # TODO: make labels work with non-SP models
      if sp is not None:
        self._getAnomalyClassifier().setParameter(
            "activeColumnCount", len(activeColumns))
        self._getAnomalyClassifier().prepareInputs()
        self._getAnomalyClassifier().compute()

        labels = self._getAnomalyClassifier().getSelf().getLabelResults()
        inferences[InferenceElement.anomalyLabel] = "%s" % labels

    inferences[InferenceElement.anomalyScore] = score
    return inferences