def __updateJobResults(self):
    """"
    Check if this is the best model
    If so:
      1) Write it's checkpoint
      2) Record this model as the best
      3) Delete the previous best's output cache
    Otherwise:
      1) Delete our output cache
     """
    isSaved = False
    while True:
      self._isBestModel, jobResults, jobResultsStr = \
                                              self.__checkIfBestCompletedModel()

      # -----------------------------------------------------------------------
      # If the current model is the best:
      #   1) Save the model's predictions
      #   2) Checkpoint the model state
      #   3) Update the results for the job
      if self._isBestModel:

        # Save the current model and its results
        if not isSaved:
          self.__flushPredictionCache()
          self._jobsDAO.modelUpdateTimestamp(self._modelID)
          self.__createModelCheckpoint()
          self._jobsDAO.modelUpdateTimestamp(self._modelID)
          isSaved = True

        # Now record the model as the best for the job
        prevBest = jobResults.get('bestModel', None)
        prevWasSaved = jobResults.get('saved', False)

        # If the current model is the best, it shouldn't already be checkpointed
        if prevBest == self._modelID:
          assert not prevWasSaved

        metrics = self._getMetrics()

        jobResults['bestModel'] = self._modelID
        jobResults['bestValue'] = metrics[self._optimizedMetricLabel]
        jobResults['metrics'] = metrics
        jobResults['saved'] = True

        isUpdated = self._jobsDAO.jobSetFieldIfEqual(self._jobID,
                                                    fieldName='results',
                                                    curValue=jobResultsStr,
                                                    newValue=json.dumps(jobResults))
        if isUpdated:
          if prevWasSaved:
            self.__deleteOutputCache(prevBest)
            self._jobsDAO.modelUpdateTimestamp(self._modelID)
            self.__deleteModelCheckpoint(prevBest)
            self._jobsDAO.modelUpdateTimestamp(self._modelID)

          self._logger.info("Model %d chosen as best model", self._modelID)
          break

      # -----------------------------------------------------------------------
      # If the current model is not the best, delete its outputs
      else:
        # NOTE: we update model timestamp around these occasionally-lengthy
        #  operations to help prevent the model from becoming orphaned
        self.__deleteOutputCache(self._modelID)
        self._jobsDAO.modelUpdateTimestamp(self._modelID)
        self.__deleteModelCheckpoint(self._modelID)
        self._jobsDAO.modelUpdateTimestamp(self._modelID)
        break