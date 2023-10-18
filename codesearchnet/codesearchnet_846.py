def _createPredictionLogger(self):
    """
    Creates the model's PredictionLogger object, which is an interface to write
    model results to a permanent storage location
    """
    # Write results to a file
    self._predictionLogger = BasicPredictionLogger(
      fields=self._model.getFieldInfo(),
      experimentDir=self._experimentDir,
      label = "hypersearch-worker",
      inferenceType=self._model.getInferenceType())

    if self.__loggedMetricPatterns:
      metricLabels = self.__metricMgr.getMetricLabels()
      loggedMetrics = matchPatterns(self.__loggedMetricPatterns, metricLabels)
      self._predictionLogger.setLoggedMetrics(loggedMetrics)