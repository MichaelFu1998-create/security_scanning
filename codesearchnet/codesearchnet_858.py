def __checkMaturity(self):
    """ Save the current metric value and see if the model's performance has
    'leveled off.' We do this by looking at some number of previous number of
    recordings """

    if self._currentRecordIndex+1 < self._MIN_RECORDS_TO_BE_BEST:
      return

    # If we are already mature, don't need to check anything
    if self._isMature:
      return

    metric = self._getMetrics()[self._optimizedMetricLabel]
    self._metricRegression.addPoint(x=self._currentRecordIndex, y=metric)

   # Perform a linear regression to see if the error is leveled off
    #pctChange = self._metricRegression.getPctChange()
    #if pctChange  is not None and abs(pctChange ) <= self._MATURITY_MAX_CHANGE:
    pctChange, absPctChange = self._metricRegression.getPctChanges()
    if pctChange  is not None and absPctChange <= self._MATURITY_MAX_CHANGE:
      self._jobsDAO.modelSetFields(self._modelID,
                                   {'engMatured':True})

      # TODO: Don't stop if we are currently the best model. Also, if we
      # are still running after maturity, we have to periodically check to
      # see if we are still the best model. As soon we lose to some other
      # model, then we should stop at that point.
      self._cmpReason = ClientJobsDAO.CMPL_REASON_STOPPED
      self._isMature = True

      self._logger.info("Model %d has matured (pctChange=%s, n=%d). \n"\
                        "Scores = %s\n"\
                         "Stopping execution",self._modelID, pctChange,
                                              self._MATURITY_NUM_POINTS,
                                              self._metricRegression._window)