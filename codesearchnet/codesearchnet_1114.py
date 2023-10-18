def _checkForOrphanedModels (self):
    """If there are any models that haven't been updated in a while, consider
    them dead, and mark them as hidden in our resultsDB. We also change the
    paramsHash and particleHash of orphaned models so that we can
    re-generate that particle and/or model again if we desire.

    Parameters:
    ----------------------------------------------------------------------
    retval:

    """

    self.logger.debug("Checking for orphaned models older than %s" % \
                     (self._modelOrphanIntervalSecs))

    while True:
      orphanedModelId = self._cjDAO.modelAdoptNextOrphan(self._jobID,
                                                self._modelOrphanIntervalSecs)
      if orphanedModelId is None:
        return

      self.logger.info("Removing orphaned model: %d" % (orphanedModelId))

      # Change the model hash and params hash as stored in the models table so
      #  that we can insert a new model with the same paramsHash
      for attempt in range(100):
        paramsHash = hashlib.md5("OrphanParams.%d.%d" % (orphanedModelId,
                                                         attempt)).digest()
        particleHash = hashlib.md5("OrphanParticle.%d.%d" % (orphanedModelId,
                                                          attempt)).digest()
        try:
          self._cjDAO.modelSetFields(orphanedModelId,
                                   dict(engParamsHash=paramsHash,
                                        engParticleHash=particleHash))
          success = True
        except:
          success = False
        if success:
          break
      if not success:
        raise RuntimeError("Unexpected failure to change paramsHash and "
                           "particleHash of orphaned model")

      # Mark this model as complete, with reason "orphaned"
      self._cjDAO.modelSetCompleted(modelID=orphanedModelId,
                    completionReason=ClientJobsDAO.CMPL_REASON_ORPHAN,
                    completionMsg="Orphaned")

      # Update our results DB immediately, rather than wait for the worker
      #  to inform us. This insures that the getParticleInfos() calls we make
      #  below don't include this particle. Setting the metricResult to None
      #  sets it to worst case
      self._resultsDB.update(modelID=orphanedModelId,
                             modelParams=None,
                             modelParamsHash=paramsHash,
                             metricResult=None,
                             completed = True,
                             completionReason = ClientJobsDAO.CMPL_REASON_ORPHAN,
                             matured = True,
                             numRecords = 0)