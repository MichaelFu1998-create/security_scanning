def _okToExit(self):
    """Test if it's OK to exit this worker. This is only called when we run
    out of prospective new models to evaluate. This method sees if all models
    have matured yet. If not, it will sleep for a bit and return False. This
    will indicate to the hypersearch worker that we should keep running, and
    check again later. This gives this worker a chance to pick up and adopt any
    model which may become orphaned by another worker before it matures.

    If all models have matured, this method will send a STOP message to all
    matured, running models (presummably, there will be just one - the model
    which thinks it's the best) before returning True.
    """
    # Send an update status periodically to the JobTracker so that it doesn't
    # think this worker is dead.
    print >> sys.stderr, "reporter:status:In hypersearchV2: _okToExit"

    # Any immature models still running?
    if not self._jobCancelled:
      (_, modelIds, _, _, _) = self._resultsDB.getParticleInfos(matured=False)
      if len(modelIds) > 0:
        self.logger.info("Ready to end hyperseach, but not all models have " \
                         "matured yet. Sleeping a bit to wait for all models " \
                         "to mature.")
        # Sleep for a bit, no need to check for orphaned models very often
        time.sleep(5.0 * random.random())
        return False

    # All particles have matured, send a STOP signal to any that are still
    # running.
    (_, modelIds, _, _, _) = self._resultsDB.getParticleInfos(completed=False)
    for modelId in modelIds:
      self.logger.info("Stopping model %d because the search has ended" \
                          % (modelId))
      self._cjDAO.modelSetFields(modelId,
                      dict(engStop=ClientJobsDAO.STOP_REASON_STOPPED),
                      ignoreUnchanged = True)

    # Update the HsState to get the accurate field contributions.
    self._hsStatePeriodicUpdate()
    pctFieldContributions, absFieldContributions = \
                                          self._hsState.getFieldContributions()


    # Update the results field with the new field contributions.
    jobResultsStr = self._cjDAO.jobGetFields(self._jobID, ['results'])[0]
    if jobResultsStr is not None:
      jobResults = json.loads(jobResultsStr)
    else:
      jobResults = {}

    # Update the fieldContributions field.
    if pctFieldContributions != jobResults.get('fieldContributions', None):
      jobResults['fieldContributions'] = pctFieldContributions
      jobResults['absoluteFieldContributions'] = absFieldContributions

      isUpdated = self._cjDAO.jobSetFieldIfEqual(self._jobID,
                                                   fieldName='results',
                                                   curValue=jobResultsStr,
                                                   newValue=json.dumps(jobResults))
      if isUpdated:
        self.logger.info('Successfully updated the field contributions:%s',
                                                              pctFieldContributions)
      else:
        self.logger.info('Failed updating the field contributions, ' \
                         'another hypersearch worker must have updated it')

    return True