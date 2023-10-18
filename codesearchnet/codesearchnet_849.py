def _updateModelDBResults(self):
    """ Retrieves the current results and updates the model's record in
    the Model database.
    """

    # -----------------------------------------------------------------------
    # Get metrics
    metrics = self._getMetrics()

    # -----------------------------------------------------------------------
    # Extract report metrics that match the requested report REs
    reportDict = dict([(k,metrics[k]) for k in self._reportMetricLabels])

    # -----------------------------------------------------------------------
    # Extract the report item that matches the optimize key RE
    # TODO cache optimizedMetricLabel sooner
    metrics = self._getMetrics()
    optimizeDict = dict()
    if self._optimizeKeyPattern is not None:
      optimizeDict[self._optimizedMetricLabel] = \
                                      metrics[self._optimizedMetricLabel]

    # -----------------------------------------------------------------------
    # Update model results
    results = json.dumps((metrics , optimizeDict))
    self._jobsDAO.modelUpdateResults(self._modelID,  results=results,
                              metricValue=optimizeDict.values()[0],
                              numRecords=(self._currentRecordIndex + 1))

    self._logger.debug(
      "Model Results: modelID=%s; numRecords=%s; results=%s" % \
        (self._modelID, self._currentRecordIndex + 1, results))

    return