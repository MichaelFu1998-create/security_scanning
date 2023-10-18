def __updateJobResultsPeriodic(self):
    """
    Periodic check to see if this is the best model. This should only have an
    effect if this is the *first* model to report its progress
    """
    if self._isBestModelStored and not self._isBestModel:
      return

    while True:
      jobResultsStr = self._jobsDAO.jobGetFields(self._jobID, ['results'])[0]
      if jobResultsStr is None:
          jobResults = {}
      else:
        self._isBestModelStored = True
        if not self._isBestModel:
          return

        jobResults = json.loads(jobResultsStr)

      bestModel = jobResults.get('bestModel', None)
      bestMetric = jobResults.get('bestValue', None)
      isSaved = jobResults.get('saved', False)

      # If there is a best model, and it is not the same as the current model
      # we should wait till we have processed all of our records to see if
      # we are the the best
      if (bestModel is not None) and (self._modelID != bestModel):
        self._isBestModel = False
        return

      # Make sure prediction output stream is ready before we present our model
      # as "bestModel"; sometimes this takes a long time, so update the model's
      # timestamp to help avoid getting orphaned
      self.__flushPredictionCache()
      self._jobsDAO.modelUpdateTimestamp(self._modelID)

      metrics = self._getMetrics()

      jobResults['bestModel'] = self._modelID
      jobResults['bestValue'] = metrics[self._optimizedMetricLabel]
      jobResults['metrics'] = metrics
      jobResults['saved'] = False

      newResults = json.dumps(jobResults)

      isUpdated = self._jobsDAO.jobSetFieldIfEqual(self._jobID,
                                                    fieldName='results',
                                                    curValue=jobResultsStr,
                                                    newValue=newResults)
      if isUpdated or (not isUpdated and newResults==jobResultsStr):
        self._isBestModel = True
        break