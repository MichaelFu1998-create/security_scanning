def updateResultsForJob(self, forceUpdate=True):
    """ Chooses the best model for a given job.

    Parameters
    -----------------------------------------------------------------------
    forceUpdate:  (True/False). If True, the update will ignore all the
                  restrictions on the minimum time to update and the minimum
                  number of records to update. This should typically only be
                  set to true if the model has completed running
    """
    updateInterval = time.time() - self._lastUpdateAttemptTime
    if updateInterval < self._MIN_UPDATE_INTERVAL and not forceUpdate:
      return

    self.logger.info("Attempting model selection for jobID=%d: time=%f"\
                     "  lastUpdate=%f"%(self._jobID,
                                        time.time(),
                                        self._lastUpdateAttemptTime))

    timestampUpdated = self._cjDB.jobUpdateSelectionSweep(self._jobID,
                                                          self._MIN_UPDATE_INTERVAL)
    if not timestampUpdated:
      self.logger.info("Unable to update selection sweep timestamp: jobID=%d" \
                       " updateTime=%f"%(self._jobID, self._lastUpdateAttemptTime))
      if not forceUpdate:
        return

    self._lastUpdateAttemptTime = time.time()
    self.logger.info("Succesfully updated selection sweep timestamp jobid=%d updateTime=%f"\
                     %(self._jobID, self._lastUpdateAttemptTime))

    minUpdateRecords = self._MIN_UPDATE_THRESHOLD

    jobResults = self._getJobResults()
    if forceUpdate or jobResults is None:
      minUpdateRecords = 0

    candidateIDs, bestMetric = self._cjDB.modelsGetCandidates(self._jobID, minUpdateRecords)

    self.logger.info("Candidate models=%s, metric=%s, jobID=%s"\
                     %(candidateIDs, bestMetric, self._jobID))

    if len(candidateIDs) == 0:
      return

    self._jobUpdateCandidate(candidateIDs[0], bestMetric, results=jobResults)